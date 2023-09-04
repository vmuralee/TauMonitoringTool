# Setup
```
cmsrel CMSSW_12_6_X
cd CMSSW_12_6_X/src
cmsenv
cd TauMonitoringTool/producer
```
# To produce a pico ntuple

The **runscript.py** allows to prepare the jobs for local submitting. Obtain nanoAOD dataset either from DAS or any local storage. If it is in DAS you can obtain list of files using following commands,
```
voms-proxy-init -voms cms
dasgoclient --query 'file dataset=<Dataset Name>' > RunFiles.txt
```
You can either run over TauID 2p1 or 2p5, by default 2p5 is used. If you need to change the tau ID make changes in the runscript.py. To prepare jobs for use the following command lines,
```
python3 runscript.py RunFiles.txt outputfile 5
```
which prepare shell script running over dataset with files splited by 5. You can change the splitting according to you, it is more safe to use maximum splitting range of 10. You can submit jobs by
```
bash localjob_submit.sh
```
After running picontuples will produce for corresponding dataset.  
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

# plot macros for comparing different efficiency graphs
`plotmacro_2inputs.py` and `plotmacro_3inputs.py` are made to compare either the same path on different datasets or different paths on the same dataset.
These macros are has the plotting style of CMS. The legend names can changed in the code itself. 
```
python3 plotmacro_2inputs.py \
--input_A Fill8102_DeepTauV2p1_New.root \
--input_B Fill8136_DeepTauV2p5_New.root \
--channel_A ditau \
--channel_B ditau \
--run "Run2022 vs Run 2023" --plot testplot --var tau_pt
```
If  the **var** argument can be *tau_pt*,*tau_eta* and *tau_phi*. In case of *tau_eta* one has to enable **--iseta** . 
# Summary of scripts in `producer`
picoNtuplizer.py makes ntuples

plotter_from_Ntuplizer.py and multiplotter_from_Ntuplizer.py both make plots using an ntuple as input (as seen above)

picoNtupler_TandP.py makes plots using nanoAOD files directly (i.e. not remade ntuples)

importantly the `obtain_histograms` function in picoNtupler_TandP.py is slightly different from the same function found in plotter_from_Ntuplizer.py

importantly the `plot` function in picoNtupler_TandP.py is used by all other files

multiplotter.py is a script that makes multiple graphs with one command (so far only ditaujet paths are supported here)

