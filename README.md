# TauMonitoringTool
Monitoring tool using NanoAOD samples

Forked from Jaime

https://github.com/jaimeleonh/TauMonitoringTool

Who forked from Vinaya

https://github.com/vmuralee/TauMonitoringTool

Plan:
add my triggers to Jaime's fork
add other code changes to Jaime's fork
PR Jaime
ask Jaime to PR all changes to Vinaya

In this repo, `producers/picoNtupler_TandP.py` is used to make turn-on plots with NanoAOD data.

The following command generates a plot of tau pT for the ditau-monitoring path, and saves it to a pdf file.  

`python3 picoNtupler_TandP.py --channel ditau --run Fill 8102 --plot testplot --var tau_pt`

The following command does the same thing, but for tau eta (necessary to include --iseta flag and change --var)

`python3 picoNtupler_TandP.py --channel ditau --run Fill 8102 --plot testplot --var tau_eta --iseta`
