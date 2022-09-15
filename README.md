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
