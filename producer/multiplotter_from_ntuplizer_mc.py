from plotter_from_ntuplizer import *
import os

#folder = "/eos/user/b/ballmond/muonNanoAOD2022D/"
folder_j = "/eos/user/j/jleonhol/picoNtuples/DY/"
folder_b = "/eos/user/b/ballmond/NanoAOD_DY/"

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
df = create_rdataframe(folders=[folder_j, folder_b])
# df = ROOT.RDataFrame("Events", "/eos/user/b/ballmond/OfficialNanoAODSamples/FullOfficialNanoAODv2p5.root")
# df = ROOT.RDataFrame("Events", "/eos/home-v/vmuralee/picoNtuples/picoNtupler2022D.root")
# df = ROOT.RDataFrame("Events", "./testntuple.root")

plotname = "dy"
label = "Run 2022"

histos = {}
channel_variables = [
    ("ditau", ["tau_pt", "tau_eta"]),
    ("ditaujet_tauleg", ["tau_pt", "tau_eta"]),
    ("ditaujet_jetleg", ["jet_pt", "jet_eta"]),
]

for channel, plottingVariables in channel_variables:
    for plottingVariable in plottingVariables:
        iseta = "eta" in plottingVariable
        histos["num_%s_%s" % (channel, plottingVariable)], histos["den_%s_%s" % (channel, plottingVariable)]\
            = obtain_histograms(df, channel, iseta, plottingVariable)

for channel, plottingVariables in channel_variables:
    for plottingVariable in plottingVariables:
        c = ROOT.TCanvas()
        histos["num_%s_%s" % (channel, plottingVariable)].Draw()
        c.SaveAs("num_%s_%s.pdf" % (channel, plottingVariable))
        c.SaveAs("num_%s_%s.png" % (channel, plottingVariable))
        histos["den_%s_%s" % (channel, plottingVariable)].Draw()
        c.SaveAs("den_%s_%s.pdf" % (channel, plottingVariable))
        c.SaveAs("den_%s_%s.png" % (channel, plottingVariable))
        del c

        plot(
            histos["num_%s_%s" % (channel, plottingVariable)],
            histos["den_%s_%s" % (channel, plottingVariable)],
            plottingVariable, channel, label, plotname
        )
