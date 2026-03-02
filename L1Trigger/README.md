# L1 TTrack ntuplizer from CMSSW producers
This repository contains the code to create ntuples containing L1 tracks for PhaseII studies:  L1Trigger/L1TTrackMatch/test/L1TrackObjectNtupleMaker_cfg.py. Small adjustement are made for the study of $X\to\tau(3\pi)\tau(3\pi)$ clustering at L1T level.

## Get started
```
cmsrel CMSSW_14_0_9
cd CMSSW_14_0_9/src
cmsenv
git cms-init
git cms-addpkg L1Trigger/TrackFindingTracklet L1Trigger/L1TTrackMatch
```
always compile with `scram b -j 8`.<\br>
Then change the number of parameters for the track reconstruction to 4->5 `l1tTTTracksFromTrackletEmulation.Hnpar = cms.Int(5)`.

## Run the ntuplizer
```
cd $CMSSW_BASE/src/L1TTrackMatch/test/
cmsRun L1TrackObjectNtupleMaker_cfg.py 
```

## Send the ntuples production on grid with CRAB
```
cd $CMSSW_BASE/src/L1TTrackMatch/production
source setup_crab.sh
python3 submit_onCrab.py -h 
```
you can follow the instructions in `L1TTrackMatch/production`
