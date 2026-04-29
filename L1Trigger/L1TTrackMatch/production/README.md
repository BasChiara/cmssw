# Ntuples prduction on CRAB
source CRAB3 and activate proxy
```
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --valid 168:00
```
or just
```
source setup_crab.sh
```
# submit on grid
submit on dataset listed in `datasample/XTauTau-3pi_PU200.yaml`
```
python3 submit_onCrab.py -e ../test/L1TrackObjectNtupleMaker_cfg.py --yaml datasample/XTauTau-3pi_PU200.yaml -t v1 -f="*TauTau*"
```
limit the number of file to process when running on MinBias sample
```
python3 submit_onCrab.py -e ../test/L1TrackObjectNtupleMaker_cfg.py --yaml datasample/XTauTau-3pi_PU200.yaml -N 2000 -t v1 -f="*MinBias*"
```
add `--dry_run` argumet to check the CRAB configuration before actually sending the jobs.