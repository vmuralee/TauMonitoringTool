#import os, sys
import ROOT
ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True)

import argparse
from plotter_from_ntuplizer import obtain_histograms


parser = argparse.ArgumentParser(description='Skim full tuple.')
parser.add_argument('--input_A', required=True, type=str, nargs='+', help="first input file")
parser.add_argument('--input_B', required=True, type=str, nargs='+', help="second input file")
parser.add_argument('--channel', required=True, type=str, 
       help="ditau, mutau, etau, VBFasymtau_uppertauleg, VBFasymtau_lowertauleg, ditaujet_tauleg, or ditaujet_jetleg,VBFditau_old")
parser.add_argument('--run', required=True, type=str, help="runs or fill used (look at your input files)")
parser.add_argument('--plot', required=True, type=str, help="plot name")
parser.add_argument('--iseta', action='store_true', help="sets flag for eat plotting")
parser.add_argument('--var', required=True, type=str, help="tau_pt, tau_eta, jet_pt, jet_eta")


possibleChannels = ["ditau", "mutau", "etau", \
                    "VBFasymtau_uppertauleg", "VBFasymtau_lowertauleg", \
                    "ditaujet_tauleg", "ditaujet_jetleg","VBFditau_old"]

def plot_comparison(h_num_os_A, h_den_os_A, h_num_os_B, h_den_os_B, plottingVariable, channel_A, channel_B, add_to_label, plotName):
    print("Plotting {} of {} and {}".format(plottingVariable, channel_A, channel_B))
    ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
    c = ROOT.TCanvas("c", "", 800, 700)

    # use multiplotter for multiple graphs
    mg = ROOT.TMultiGraph("mg", "")

    # this divides num by den.
    # the "Clopper-Pearson" interval is not supported for
    # TGraphAsymmErrors::Divide, so i changed "cp" to "n"
    # the graphs are not changed
    # https://root.cern.ch/doc/master/classTGraphAsymmErrors.html#a37a202762b286cf4c7f5d34046be8c0b
    # use "nv" to get per-bin efficiency printed to terminal
    gr_A = ROOT.TGraphAsymmErrors(h_num_os_A.GetPtr(),h_den_os_A.GetPtr(), "n")
    gr_A.SetTitle("")
    gr_A.SetLineColor(2) # this is red
    gr_A.SetMarkerStyle(21) # this is a filled box
    gr_A.SetMarkerSize(1.5)


    gr_B = ROOT.TGraphAsymmErrors(h_num_os_B.GetPtr(),h_den_os_B.GetPtr(), "n")
    gr_B.SetTitle("")
    gr_B.SetLineColor(9) # this is blue
    gr_B.SetMarkerStyle(20) # this is a filled circle
    gr_B.SetMarkerColor(12) # this is a light grey
    gr_B.SetMarkerSize(1.4)

    mg.Add(gr_A)
    mg.Add(gr_B)
    # "P" forces the use of the chosen marker
    # "A" draws without the axis 
    # somehow the plot is not drawn without this argument
    # https://root.cern/doc/master/classTHistPainter.html#HP01a
    mg.Draw("AP")

    label = ROOT.TLatex(); label.SetNDC(True)
    if(plottingVariable == "tau_pt" or plottingVariable=="tau_l1pt"):
        label.DrawLatex(0.8, 0.03, "#tau_{pT}")
    elif(plottingVariable == "jet_pt"):
        label.DrawLatex(0.8, 0.03, "jet_{pT}")
    elif(plottingVariable == "jet_eta"):
        label.DrawLatex(0.8, 0.03, "#eta_{jet}")
    else:
        label.DrawLatex(0.8, 0.03, "#eta_{#tau}")
    label.SetTextSize(0.040); label.DrawLatex(0.100, 0.920, "#bf{CMS Run3 Data}")
    label.SetTextSize(0.030); label.DrawLatex(0.630, 0.920, "#sqrt{s} = 13.6 TeV, %s" % add_to_label)

    # add legend
    leg = ROOT.TLegend(0.55, 0.15, 0.90, 0.45)
    leg.SetTextSize(0.045)
    leg.AddEntry(gr_A, channel_A)
    leg.AddEntry(gr_B, channel_B)
    leg.Draw()
    # add new leg
    # make user friendly

    combined_name = channel_A + "_" + channel_B
    c.SaveAs("%s_%s_%s.pdf" % (plotName, combined_name, plottingVariable))
    c.SaveAs("%s_%s_%s.png" % (plotName, combined_name, plottingVariable))


if __name__ == "__main__":

    args = parser.parse_args()
    channel = args.channel
    #iseta = args.iseta
    plottingVariable = args.var
    iseta = "eta" in "plottingVariable"
    print(iseta)
    print(args.input_A, args.input_B)
    df_A = ROOT.RDataFrame("Events",tuple(args.input_A))
    h_num_os_A, h_den_os_A = obtain_histograms(df_A, "VBFditau_old", iseta, plottingVariable)
    df_B = ROOT.RDataFrame("Events",tuple(args.input_B))
    h_num_os_B, h_den_os_B = obtain_histograms(df_B, "mutau", iseta, plottingVariable)

    plot_comparison(h_num_os_A, h_den_os_A, h_num_os_B, h_den_os_B, plottingVariable, "VBFditau_old", "mutau", args.run, args.plot)
