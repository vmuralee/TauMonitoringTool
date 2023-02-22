from plotter_from_ntuplizer import *

#folder = "/eos/user/b/ballmond/muonNanoAOD2022D/"
folder = "/eos/user/j/jleonhol/muonNanoAOD2022E/"

def create_rdataframe(folders=None, inputFiles=None):
    if not inputFiles:
        inputFiles = []
        for folder in folders:
            files = os.listdir(folder)
            inputFiles += [folder + f for f in files if f.endswith(".root")]
    print(inputFiles)
    return ROOT.RDataFrame("Events", tuple(inputFiles))
df = create_rdataframe(folders=[folder])
# df = ROOT.RDataFrame("Events", "/eos/user/b/ballmond/OfficialNanoAODSamples/FullOfficialNanoAODv2p5.root")
# df = ROOT.RDataFrame("Events", "/eos/home-v/vmuralee/picoNtuples/picoNtupler2022D.root")
# df = ROOT.RDataFrame("Events", "./testntuple.root")

plotname = "muon2022e_notrigobj"
label = "Muon - 2022E (no trig. obj.)"

histos = {}
channel_variables = [
    ("ditau", ["tau_pt", "tau_eta"]),
    ("mutau", ["tau_pt", "tau_eta"]),
    ("VBFasymtau_uppertauleg", ["tau_pt", "tau_eta"]),
    ("VBFasymtau_lowertauleg", ["tau_pt", "tau_eta"]),
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
