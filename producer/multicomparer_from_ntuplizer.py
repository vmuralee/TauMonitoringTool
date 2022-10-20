from plotter_from_ntuplizer import *
from plot_comparison import plot_comparison

# folders = ["/eos/user/b/ballmond/muonNanoAOD2022D/", "/eos/user/j/jleonhol/muonNanoAOD2022D_notrigobj/"]
folders = ["/eos/user/j/jleonhol/muonNanoAOD2022D_notrigobj/", "/eos/user/j/jleonhol/muonNanoAOD2022E/"]
# legends = ["w/ offl-trigger matching", "w/o offl-trigger matching"]
legends = ["Run2022D (no match)", "Run2022E (no match)"]

def create_rdataframe(folders=None, inputFiles=None):
    if not inputFiles:
        inputFiles = []
        for folder in folders:
            files = os.listdir(folder)
            inputFiles += [os.path.join(folder, f) for f in files if f.endswith(".root")]
    print(inputFiles)
    return ROOT.RDataFrame("Events", tuple(inputFiles))

dfs = [create_rdataframe(folders=[folder]) for folder in folders]

# plotname = "comparison_muon2022d"
# label = "Muon - 2022D"

plotname = "comparison_muon2022de"
label = "Muon - 2022D/E"


histos = []
channel_variables = [
    ("ditau", ["tau_pt", "tau_eta"]),
    ("ditaujet_tauleg", ["tau_pt", "tau_eta"]),
    ("ditaujet_jetleg", ["jet_pt", "jet_eta"]),
]

for df in dfs:
    histos.append({})
    for channel, plottingVariables in channel_variables:
        for plottingVariable in plottingVariables:
            iseta = "eta" in plottingVariable
            histos[-1]["num_%s_%s" % (channel, plottingVariable)], histos[-1]["den_%s_%s" % (channel, plottingVariable)]\
                = obtain_histograms(df, channel, iseta, plottingVariable)

for channel, plottingVariables in channel_variables:
    for plottingVariable in plottingVariables:
        plot_comparison(
            histos[0]["num_%s_%s" % (channel, plottingVariable)],
            histos[0]["den_%s_%s" % (channel, plottingVariable)],
            histos[1]["num_%s_%s" % (channel, plottingVariable)],
            histos[1]["den_%s_%s" % (channel, plottingVariable)],
            plottingVariable,
            channel,
            channel,
            label,
            plotname,
            legends)
