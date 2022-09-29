from plotter_from_ntuplizer import *

df = ROOT.RDataFrame("Events", "/eos/user/b/ballmond/OfficialNanoAODSamples/FullOfficialNanoAODv2p5.root")

plotname = "officialplot"
label = "Muon 2022D"

histos = {}
channel_variables = [
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
