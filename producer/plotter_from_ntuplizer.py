import os, sys
import ROOT
ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True)

import argparse
from picoNtupler_TandP import plot
from RooPlottingTool import *


parser = argparse.ArgumentParser(description='Skim full tuple.')
parser.add_argument('--input', required=True, type=str, nargs='+', help="input files")
parser.add_argument('--channel', required=True, type=str, 
       help="ditau, mutau, etau, \
             VBFasymtau_uppertauleg, VBFasymtau_lowertauleg, \
             ditaujet_tauleg, ditaujet_jetleg, \
             VBFditau_old, VBFditau_Run3_tauleg")
parser.add_argument('--run', required=True, type=str, help="runs or fill used (look at your input files)")
parser.add_argument('--plot', required=True, type=str, help="plot name")
parser.add_argument('--iseta', action='store_true', help="sets flag for eat plotting")
parser.add_argument('--var', required=True, type=str, help="tau_pt, tau_eta, jet_pt, jet_eta")


possibleChannels = ["ditau", "mutau", "etau", \
                    "VBFasymtau_uppertauleg", "VBFasymtau_lowertauleg", \
                    "ditaujet_tauleg", "ditaujet_jetleg", \
                    "VBFditau_old", "VBFditau_Run3_tauleg"]


def obtain_histograms(df, channel, iseta, plottingVariable, additional_selection=None):

    if additional_selection:
        df = df.Filter(additional_selection)

    df = df.Filter("Muon_Index >= 0 && muon_iso < 0.1 && Tau_goodid == 1")

    if channel != "ditaujet_jetleg":
        assert "jet" not in plottingVariable
        df = df.Filter("passZmass == 1").Define("tau_pt", "Tau_pt[Tau_Index]").Define("tau_eta", "Tau_eta[Tau_Index]")
        if iseta:
          df = df.Filter('tau_pt > 35')  
        h_den_os = df.Histo1D(CreateHistModel("denominator", iseta), plottingVariable)
        # numerator histogram
        if channel == 'ditau':
            # HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1 == 1").Histo1D( \
            h_num_os = df.Filter("pass_ditau >= 0 && \
                HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1 == 1").Histo1D(
                # HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1 == 1").Filter("TrigObj_l1pt.at(pass_ditau) >= 26 && TrigObj_l1iso.at(pass_ditau) > 0").Histo1D( \
                CreateHistModel("numerator", iseta), plottingVariable, 'weight')

        elif channel == 'mutau':
            h_num_os = df.Filter("pass_mutau >= 0 && \
                HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1 == 1").Histo1D( \
                CreateHistModel("numerator", iseta), plottingVariable, 'weight')

        elif channel == 'VBFasymtau_uppertauleg':
            h_num_os = df.Filter("pass_VBFasymtau_uppertauleg >= 0 && \
                         HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS45_L2NN_eta2p1_CrossL1 == 1").Histo1D( \
                         CreateHistModel("numerator", iseta), plottingVariable, 'weight')

        #FIXME: this should be lowertauleg, right?
        elif channel == 'VBFasymtau_lowertauleg':
            h_num_os = df.Filter("pass_VBFasymtau_uppertauleg >= 0 && \
                         HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS20_eta2p1_SingleL1 == 1").Histo1D( \
                         CreateHistModel("numerator", iseta), plottingVariable, 'weight')

        #FIXME: this is Run2 mutau monitoring path, update everywhere
        elif channel == 'VBFditau_old':
            h_num_os = df.Filter("pass_VBFasymtau_uppertauleg >= 0 && \
                         HLT_IsoMu20_eta2p1_TightChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1 == 1").Histo1D( \
                         CreateHistModel("numerator", iseta), plottingVariable, 'weight')

        elif channel == 'VBFditau_Run3_tauleg':
            h_num_os = df.Filter("pass_VBFditau_Run3_tauleg >= 0 && \
                         HLT_IsoMu27_MediumDeepTauPFTauHPS20_eta2p1_SingleL1 == 1").Histo1D( \
                         CreateHistModel("numerator", iseta), plottingVariable, 'weight')
                         #HLT_IsoMu20_eta2p1_TightChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1 == 1").Histo1D( \

        elif channel == 'ditaujet_tauleg':
            h_num_os = df.Filter("pass_ditau >= 0 && \
                         HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_CrossL1 == 1"
                         ).Filter("TrigObj_l1pt.at(pass_ditau) >= 26 && TrigObj_l1iso.at(pass_ditau) > 0"
                         ).Histo1D(CreateHistModel("numerator", iseta), plottingVariable, 'weight')

    else:
        assert "jet" in plottingVariable
        df = df.Filter("Jet_Index >= 0"
            ).Define("jet_pt","Jet_pt[Jet_Index]"
            ).Define("jet_eta","Jet_eta[Jet_Index]"
            ).Filter("pass_ditau > 0 && HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_CrossL1 == 1"
            ).Filter("TrigObj_l1pt.at(pass_ditau) >= 26 && TrigObj_l1iso.at(pass_ditau) > 0")
        h_den_os = df.Histo1D(CreateHistModel("denominator", iseta, True), plottingVariable)
        h_num_os = df.Filter("pass_ditau_jet >= 0 && \
                     HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_PFJet60_CrossL1 == 1").Histo1D( \
                     CreateHistModel("numerator", iseta, True), plottingVariable)
    return h_num_os, h_den_os


if __name__ == "__main__":

    args = parser.parse_args()
    channel = args.channel
    iseta = args.iseta
    plottingVariable = args.var
    print(args.input)
    df = ROOT.RDataFrame("Events",tuple(args.input))
    h_num_os, h_den_os = obtain_histograms(df, channel, iseta, plottingVariable)
    plot(h_num_os, h_den_os, plottingVariable, channel, args.run, args.plot)
