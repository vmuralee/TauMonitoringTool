import os
from plotter_from_ntuplizer import *
from plot_comparison import plot_comparison

# folders = ["/eos/user/b/ballmond/muonNanoAOD2022D/", "/eos/user/j/jleonhol/muonNanoAOD2022D_notrigobj/"]
# folders = ["/eos/user/j/jleonhol/muonNanoAOD2022D_notrigobj/", "/eos/user/j/jleonhol/muonNanoAOD2022E/"]
#folders = ["/eos/user/j/jleonhol/muonNanoAOD2022D_notrigobj/", "/eos/user/j/jleonhol/muonNanoAOD2022E/", "/eos/user/j/jleonhol/muonNanoAOD2022F/"]
# folders = ["/eos/user/j/jleonhol/muonNanoAOD2022F/", "/eos/user/j/jleonhol/muonNanoAOD2022F/"]
folders = ["/eos/user/j/jleonhol/muonNanoAOD2022E/", "/eos/user/j/jleonhol/muonNanoAOD2022F/", "/eos/user/j/jleonhol/muonNanoAOD2022G_V11/", ["/eos/user/j/jleonhol/muonNanoAOD2022C_notrigobj/", "/eos/user/j/jleonhol/muonNanoAOD2022D_notrigobj/"], ]
# legends = ["w/ offl-trigger matching", "w/o offl-trigger matching"]
legends = ["2022E", "2022F", "2022G", "2022preTS1"]
# legends = ["Run < 361514", "Run >= 361514"]

# additional_selections = ["run < 361514", "run >= 361514"]
additional_selections = []

plotname = "comparison_muon2022preDEFG"
label = "2022 C/D/E/F/G"

def create_rdataframe(folders=None, inputFiles=None):
    if not inputFiles:
        inputFiles = []
        for folder in folders:
            if isinstance(folder, list):
                files = []
                for folderp in folder:
                    filesp = os.listdir(folderp)
                    files += [os.path.join(folderp, f) for f in filesp]
            else:
                files = [os.path.join(folder, f)  for f in os.listdir(folder)]

            for f in files:
                try:
                    tf = ROOT.TFile.Open(f)
                    tree = tf.Get("Events")
                    entries = tree.GetEntries()
                    inputFiles.append(f)
                except:
                    print("%s not available" % f)
    # if "/eos/user/j/jleonhol/muonNanoAOD2022F/outntuple_2p5_10.root" in inputFiles:
        # inputFiles.remove("/eos/user/j/jleonhol/muonNanoAOD2022F/outntuple_2p5_10.root")
    print(inputFiles)
    return ROOT.RDataFrame("Events", tuple(inputFiles))

dfs = [create_rdataframe(folders=[folder]) for folder in folders]

# plotname = "comparison_muon2022d"
# label = "Muon - 2022D"


histos = {"num": {}, "den": {}}
channel_variables = [
    ("ditau", ["tau_pt", "tau_eta"]),
    ("mutau", ["tau_pt", "tau_eta"]),
    ("VBFasymtau_uppertauleg", ["tau_pt", "tau_eta"]),
    ("VBFasymtau_lowertauleg", ["tau_pt", "tau_eta"]),
    ("VBFditau_Run3_tauleg", ["tau_pt", "tau_eta"]),
    ("ditaujet_tauleg", ["tau_pt", "tau_eta"]),
    ("ditaujet_jetleg", ["jet_pt", "jet_eta"]),
]

for channel, plottingVariables in channel_variables:
    for plottingVariable in plottingVariables:
        histos["num"]["%s_%s" % (channel, plottingVariable)] = []
        histos["den"]["%s_%s" % (channel, plottingVariable)] = []
        for idf, df in enumerate(dfs):
            if len(dfs) == len(additional_selections):
                additional_selection = additional_selections[idf]
            else:
                additional_selection = None
            histos["num"]["%s_%s" % (channel, plottingVariable)].append(None)
            histos["den"]["%s_%s" % (channel, plottingVariable)].append(None)
            iseta = "eta" in plottingVariable
            histos["num"]["%s_%s" % (channel, plottingVariable)][-1],\
            histos["den"]["%s_%s" % (channel, plottingVariable)][-1] \
                = obtain_histograms(df, channel, iseta, plottingVariable, additional_selection)

for channel, plottingVariables in channel_variables:
    for plottingVariable in plottingVariables:
        plot_comparison(
            histos["num"]["%s_%s" % (channel, plottingVariable)],
            histos["den"]["%s_%s" % (channel, plottingVariable)],
            plottingVariable,
            [channel],
            label,
            plotname,
            legends)
