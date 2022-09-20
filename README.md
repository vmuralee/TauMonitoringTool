# To produce the pico ntuple
First to produce the pico ntuple using the `picoNtuplizer.py` with arguments of  2p1(2p5) depends on the old tauID(new) and output ntuple name \
```python3 picoNtuplizer.py 2p1 picoNtuple```

# To produce the plot
The following command generates a plot of tau pT for the ditau-monitoring path, and saves it to a pdf file.  \
```
python3 plotter_from_ntuplizer.py --input picoNtuple.root --channel ditau --run "Fill 8102" --plot testplot --var tau_pt
```
The following command does the same thing, but for tau eta (necessary to include --iseta flag and change --var)
```
python3 plotter_from_ntuplizer.py --input picoNtuple.root --channel ditau --run "Fill 8102" --plot testplot --var tau_eta --iseta
```

`plot_comparison.py` is made to compare either the same path on different datasets or different paths on the same dataset.
For now, the legend lable of the script is hardcoded, so the first sample is always written as using DeepTau v2p1
and the second as using DeepTau v2p5.
To use plot_comparison.py in this way, first produce two different ntuples using picoNtuplizer.py with 2p1 and 2p5, then run the following command.
```
python3 plot_comparison.py \
--input_A Fill8102_DeepTauV2p1_New.root \
--input_B Fill8136_DeepTauV2p5_New.root \
--channel_A VBFditau_Run3_tauleg \
--channel_B VBFditau_Run3_tauleg \
--run "Compare DeepTau" --plot testplot --var tau_pt
```

# Summary of scripts in `producer`
picoNtuplizer.py makes ntuples

plotter_from_Ntuplizer.py and multiplotter_from_Ntuplizer.py both make plots using an ntuple as input (as seen above)

picoNtupler_TandP.py makes plots using nanoAOD files (i.e. not remade ntuples)

importantly the `obtain_histograms` function in picoNtupler_TandP.py is slightly different from the same function found in plotter_from_Ntuplizer.py

importantly the `plot` function in picoNtupler_TandP.py is used by all other files

multiplotter.py is a script that makes multiple graphs (so far only ditaujet paths are supported here)

