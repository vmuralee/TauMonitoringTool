from plotter_from_ntuplizer import *

df = ROOT.RDataFrame("Events", "picoNtuple.root")

plotname = "testplot"
label = "Fill 8136"

histos = {}
channel_variables = [
    ("ditaujet_tauleg", ["tau_pt", "tau_eta"]),
    ("ditaujet_jetleg", ["jet_pt", "jet_eta"]),
]

for channel, plottingVariables in channel_variables:
    for plottingVariable in plottingVariables:
        iseta = "eta" in plottingVariable
        histos["num_%s" % plottingVariable], histos["den_%s" % plottingVariable] = obtain_histograms(df, channel, iseta, plottingVariable)

for channel, plottingVariables in channel_variables:
    for plottingVariable in plottingVariables:
        plot(histos["num_%s" % plottingVariable], histos["den_%s" % plottingVariable], plottingVariable, channel, label, plotname)