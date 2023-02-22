# To produce a pico ntuple
To produce the pico ntuple using the `picoNtuplizer.py` with arguments of  2p1(2p5) depends on the old tauID(new) and output ntuple name \
```python3 picoNtuplizer.py tauIDversion output_name list_of_input_files.txt```
TauID versions 2p1 and 2p5 are supported. If you're input file list is named "input_files.txt" use the following command.
```python3 picoNtuplizer.py 2p5 picoNtuple input_files.txt```

# To produce the plot
The following command generates a plot of tau pT for the ditau-monitoring path, and saves it to a png and pdf file.  \

```
python3 plotter_from_ntuplizer.py \
--input /eos/user/b/ballmond/muonNanoAOD2022D/\*.root \
--channel VBFasymtau_uppertauleg \
--data_label "Muon2022D" \
--plot testplot \
--var tau_pt
```

Above, the `input` field is all available NanoAOD Muon2022D data.
The `channel` is a shorthand to select a supported tau HLT. Available channels are
["ditau", "mutau", "etau",                           <- standard tau monitoring paths, etau not yet implemented
"VBFasymtau_uppertauleg", "VBFasymtau_lowertauleg",  <- two paths to monitor the new VBF asym ditau path, seeded by an L1 IsoTau
"ditaujet_tauleg", "ditaujet_jetleg",                <- two paths to monitor the new ditau+jet path
"VBFditau_old", "VBFditau_Run3_tauleg"]              <- two extra paths with implemented support
`data_label` will appear on the top right of the graph and describes the dataset used.
`plot` takes any string argument and prepends it to your generated graph file.
Finally, `var` can be set to `tau_pt` or `tau_eta` and switches which variable is plotted (jet_pt and jet_eta are not supported for all paths).  

# Additional functionality
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

picoNtupler_TandP.py makes plots using nanoAOD files directly (i.e. not remade ntuples)

importantly the `obtain_histograms` function in picoNtupler_TandP.py is slightly different from the same function found in plotter_from_Ntuplizer.py

importantly the `plot` function in picoNtupler_TandP.py is used by all other files

multiplotter.py is a script that makes multiple graphs with one command (so far only ditaujet paths are supported here)

