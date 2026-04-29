import yaml
import datetime
from fnmatch import fnmatch
from argparse import ArgumentParser
import os

#CRAB 
import CRABClient
from CRABClient.UserUtilities import config, ClientException
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from http.client import HTTPException

def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print("Failed submitting task:",hte.headers)
        except ClientException as cle:
            print("Failed submitting task:",cle)

if __name__ == '__main__':


    parser = ArgumentParser()
    parser.add_argument('-e', '--executable', 
                        default = '../test/L1TrackObjectNtupleMaker_cfg.py', 
                        help = 'Configuration file to bexecuted via `cmsRun` on the grid')
    parser.add_argument('-y', '--yaml', 
                        required=True,
                        help = 'File with dataset descriptions')
    parser.add_argument('--runOnFiles',
                        action='store_true',
                        help = 'Run on files instead of DAS datasets. The YAML file should point also to the .txt with the list of files to be processed')
    parser.add_argument('-N', '--Nmax',
                        type=int,
                        default = -1,
                        help = 'Number of Units (files/LS...) to be processed. If -1, all units will be processed') 
    parser.add_argument('-o', '--output_dir', 
                        default = '/store/group/phys_bphys/cbasile/BsTauTau-L1Scouting', 
                        help = 'output directory for the jobs - without /eos/cms prefix')
    parser.add_argument('-t', '--tag',  
                        default = '', 
                        help = 'tag to mark the jobs')
    parser.add_argument('-f', '--filter', 
                        default='*', 
                        help = 'filter samples, POSIX regular expressions allowed')
    parser.add_argument('-d', '--dry_run', 
                        action='store_true')
    args = parser.parse_args()

    #fixme: set the job tag in the requestName  
    production_tag = '_'.join(['L1TTrackMatch', args.tag]) 

    config = config()
    config.section_('General')
    config.General.transferOutputs = True
    config.General.transferLogs = True
    config.General.workArea = production_tag

    config.section_('Data')
    config.Data.publication = False
    config.Data.outLFNDirBase = os.path.join(args.output_dir, config.General.workArea) 
    # check on DAS the DBS
    config.Data.inputDBS = 'global'
    #config.Data.inputDBS = 'phys03'
    
    config.section_('JobType')
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = args.executable
    config.JobType.numCores=2
    config.JobType.maxMemoryMB = 5000 # MAX 2500*numCores
    config.JobType.allowUndistributedCMSSW = True

    config.section_('User')
    config.section_('Site')
    config.Site.storageSite = 'T2_CH_CERN' # /eos/

    
    # parse the YAML file with the dataset descriptions
    with open(args.yaml) as f:
        doc  = yaml.load(f,Loader=yaml.FullLoader) # Parse YAML file
    common  = doc['common'] if 'common' in doc else {}
    samples = doc['samples'] if 'samples' in doc else {}
    if not samples:
        print('[ERROR] NO samples found in the YAML file!')
        exit(1)
    
    # loop over samples
    for sample, s_info in samples.items():
        
        # Filter names according to what we need
        if not fnmatch(sample, args.filter): continue
        print(f'[+++] submitting {sample}')
        isMC = s_info.get('isMC', False)
        common_branch = 'mc' if isMC else 'data'
        
        if args.runOnFiles: # run on a list of files
            flist = s_info.get('filelist', None)
            if not (flist and os.path.isfile(flist)):
                print(f'[ERROR] File-list {flist} not found for {sample} or file does not exist!')
                continue
            config.Data.userInputFiles = open(flist).readlines()[:args.Nmax] if args.Nmax > 0 else open(flist).readlines()
            config.Data.outputPrimaryDataset = s_info.get('dataset', sample).split('/')[0]
            config.Site.whitelist = 'T2_*'
        else: # run on the full dataset
            config.Data.inputDataset   = s_info['dataset']
            config.General.requestName = sample
            if args.Nmax > 0: config.Data.totalUnits = args.Nmax
        
        config.Data.splitting = 'FileBased' if isMC or args.runOnFiles else 'LumiBased'
        config.Data.unitsPerJob = s_info.get('splitting', common[common_branch].get('splitting', None))
        config.Data.lumiMask = s_info.get('lumimask',  common[common_branch].get('lumimask', None)) if not isMC else ''
        
        globaltag = s_info.get( 'globaltag', common[common_branch].get('globaltag', None)) # FIXME : not used -> hardcoded in the executable
        
        config.JobType.outputFiles = ['L1TrackObject_output.root']

        print()
        print(config)
        if not args.dry_run: submit(config)
