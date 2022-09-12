import os
import sys

import ROOT

# Enable multi-threading                                                                                                                                                                                    
ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True)

import argparse

parser = argparse.ArgumentParser(description='Skim full tuple.')
parser.add_argument('--input', required=False, type=str, nargs='+', help="input files")
parser.add_argument('--channel', required=True, type=str, 
       help="ditau, mutau, etau, VBFasymtau_uppertauleg, VBFasymtau_lowertauleg, ditaujet_tauleg, or ditaujet_jetleg")
parser.add_argument('--run', required=True, type=str, help="runs or fill used (look at your input files)")
parser.add_argument('--plot', required=True, type=str, help="plot name")
parser.add_argument('--iseta', action='store_true', help="sets flag for eat plotting")
parser.add_argument('--var', required=True, type=str, help="tau_pt, tau_eta, jet_pt, jet_eta")



possibleChannels = ["ditau", "mutau", "etau", \
                    "VBFasymtau_uppertauleg", "VBFasymtau_lowertauleg", \
                    "ditaujet_tauleg", "ditaujet_jetleg"]

core_dir = str(os.getcwd()).split('producer')

Trigger_header_path = os.path.join(core_dir[0] + '/interface' + os.sep, "picoNtupler.h")

ROOT.gInterpreter.Declare('#include "{}"'.format(Trigger_header_path))

sys.path.insert(1, core_dir[0]+'/python')

from RooPlottingTool import *


def create_rdataframe(folders, inputFiles=None):
    if not inputFiles:
        inputFiles = []
        for folder in folders:
            files = os.listdir(folder)
            inputFiles += [folder + f for f in files]

    return ROOT.RDataFrame("Events", tuple(inputFiles))

def obtain_histograms(df, channel, iseta, plottingVariable):

    if channel not in possibleChannels:
        print("{} is not a valid channel. Input must be one of the following {}".format(channel, possibleChannels))
        sys.exit()

    # Tag And Probe selection {Obtaining high pure Z -> mu tau Events}
    ## select muon (Tag) candidate 
    df_tag = df.Filter("nMuon == 1 && nTau >=1").Define("Muon_Index",\
              "MuonIndex(nTrigObj, TrigObj_id, TrigObj_filterBits, TrigObj_pt, TrigObj_eta, TrigObj_phi,\
               nMuon, Muon_pt, Muon_eta, Muon_phi, Muon_mass, Muon_pfRelIso04_all)").Define("muon_p4",\
              "Obj_p4(Muon_Index, Muon_pt, Muon_eta, Muon_phi, Muon_mass)").Define("muon_iso","getFloatValue(Muon_pfRelIso04_all, Muon_Index)")

    ## select tau (probe) candidate
    df_probe = df_tag.Filter("Muon_Index >= 0 && muon_iso < 0.1 && HLT_IsoMu24_eta2p1 == 1").Define("Tau_Index",\
                 "TauIndex(nTau, Tau_pt, Tau_eta, Tau_phi, Tau_mass, Tau_dz, muon_p4)")

    df_probe_id = df_probe.Filter("Tau_Index >= 0 && \
                                   Tau_decayMode[Tau_Index] != 5 && Tau_decayMode[Tau_Index] != 6 && Tau_idDeepTau2018v2p5VSjet[Tau_Index]==5").Define("tau_p4","Obj_p4(Tau_Index, Tau_pt, Tau_eta, Tau_phi, Tau_mass)")
    #  Tau_idDeepTau2017v2p1VSjet[Tau_Index] >=16

    # Calculate Efficiency

    # denominator histogram
    if channel != 'ditaujet_jetleg':
        ## select mu-tau pair with os and ss events
        df_TandP_os = df_probe_id.Define('weight',\
                    "(Tau_charge[Tau_Index] != Muon_charge[Muon_Index]) ? 1. : -1.").Define("mT",\
                    "CalcMT(muon_p4, MET_pt, MET_phi)").Define("m_vis", "ZMass(tau_p4, muon_p4)")

        ## select pure Z -> mu tau events
        df_TandP = df_TandP_os.Filter("mT < 30 && m_vis > 40 && m_vis < 80").Define("tau_pt",\
                                      "Tau_pt[Tau_Index]").Define("tau_eta", "Tau_eta[Tau_Index]")
        df_TandP_den_filt = df_TandP
        h_den_os = df_TandP_den_filt.Histo1D(CreateHistModel("denominator", iseta), plottingVariable)

    else:
        assert "jet" in plottingVariable 
        df_TandP_den = df_probe_id.Define("pass_ditau",
            "PassDiTauFilter(nTrigObj, TrigObj_id, TrigObj_filterBits, TrigObj_pt, TrigObj_eta, TrigObj_phi,\
             Tau_pt[Tau_Index], Tau_eta[Tau_Index], Tau_phi[Tau_Index])")

        # df_TandP_den = df_TandP_den.Define("Jet_Index", \
        #                 "JetIndex(nJet, Jet_pt, Jet_eta, Jet_phi, Jet_mass, \
        #                  Jet_puId, Jet_jetId, muon_p4, tau_p4)" # PU ID not present in this nanoAOD, skipped

        df_TandP_den = df_TandP_den.Define("Jet_Index", "JetIndex(nJet, Jet_pt, Jet_eta, Jet_phi, Jet_mass, Jet_jetId, muon_p4, tau_p4)"
            ).Filter("Jet_Index >= 0").Define("jet_pt","Jet_pt[Jet_Index]").Define("jet_eta","Jet_eta[Jet_Index]")

        df_TandP_den_filt = df_TandP_den.Filter("pass_ditau > 0.5 && HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_CrossL1 == 1")
        h_den_os = df_TandP_den_filt.Histo1D(CreateHistModel("denominator", iseta), plottingVariable)

    # define numerators used more than once below
    PassMuTauFilter = "PassMuTauFilter(nTrigObj, TrigObj_id, TrigObj_filterBits, \
                       TrigObj_pt, TrigObj_eta, TrigObj_phi, \
                       Tau_pt[Tau_Index], Tau_eta[Tau_Index], Tau_phi[Tau_Index])"

    PassDiTauFilter = "PassDiTauFilter(nTrigObj, TrigObj_id, TrigObj_filterBits, \
                       TrigObj_pt, TrigObj_eta, TrigObj_phi, \
                       Tau_pt[Tau_Index], Tau_eta[Tau_Index], Tau_phi[Tau_Index])"

    # numerator histogram
    if channel == 'ditau':
        df_TandP_num = df_TandP_den_filt.Define("pass_ditau", PassDiTauFilter)
        h_num_os = df_TandP_num.Filter("pass_ditau > 0.5 && \
        HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1 == 1").Histo1D(CreateHistModel("numerator", iseta), plottingVariable, 'weight')


    elif channel == 'mutau':
        df_TandP_num = df_TandP_den_filt.Define("pass_mutau", PassMuTauFilter)

        h_num_os = df_TandP_num.Filter("pass_mutau > 0.5 && \
                     HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1 == 1").Histo1D( \
                     CreateHistModel("numerator", iseta), plottingVariable, 'weight')

    elif channel == 'VBFasymtau_uppertauleg':
        df_TandP_num = df_TandP_den_filt.Define("pass_VBFasymtau_uppertauleg", PassMuTauFilter)

        h_num_os = df_TandP_num.Filter("pass_VBFasymtau_uppertauleg > 0.5 && \
                     HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS45_L2NN_eta2p1_CrossL1 == 1").Histo1D( \
                     CreateHistModel("numerator", iseta), plottingVariable, 'weight')

    elif channel == 'VBFasymtau_lowertauleg':
        df_TandP_num = df_TandP_den_filt.Define("pass_VBFasymtau_uppertauleg", PassMuTauFilter)

        h_num_os = df_TandP_num.Filter("pass_VBFasymtau_uppertauleg > 0.5 && \
                     HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS20_eta2p1_SingleL1 == 1").Histo1D( \
                     CreateHistModel("numerator", iseta), plottingVariable, 'weight')

    elif channel == 'ditaujet_tauleg':
        df_TandP_num = df_TandP_den_filt.Define("pass_ditau", PassDiTauFilter)

        h_num_os = df_TandP_num.Filter("pass_ditau > 0.5 && \
                     HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_CrossL1 == 1").Histo1D( \
                     CreateHistModel("numerator", iseta), plottingVariable, 'weight')

    elif channel == 'ditaujet_jetleg':
        df_TandP_num = df_TandP_den_filt.Define("pass_ditau_jet",\
                "PassDiTauJetFilter(nTrigObj, TrigObj_id, TrigObj_filterBits, TrigObj_pt, TrigObj_eta, TrigObj_phi, \
                 Jet_pt[Jet_Index], Jet_eta[Jet_Index], Jet_phi[Jet_Index])")

        h_num_os = df_TandP_num.Filter("pass_ditau_jet > 0.5 && \
                     HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_PFJet60_CrossL1 == 1").Histo1D( \
                     CreateHistModel("numerator", iseta), plottingVariable) 
    else:
        raise ValueError()

    return h_num_os, h_den_os


def plot(h_num_os, h_den_os, plottingVariable, channel, add_to_label, plotName):

    ## Produce plot                 
    print("Create TurnON")                                                                                                                                                                         
    ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
    c = ROOT.TCanvas("c", "", 800, 700)

    gr = ROOT.TEfficiency(h_num_os.GetPtr(),h_den_os.GetPtr())
    gr.SetTitle("")
    gr.Draw()

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

    c.SaveAs("%s_%s_%s.pdf" % (plotName, channel, plottingVariable))


if __name__ == '__main__':
    args = parser.parse_args()
    channel = args.channel
    iseta = args.iseta
    plottingVariable = args.var

    #inputFiles = (f'/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/anayak/2022NanoAOD/SingleMuonV1/Files2/nano_aod_{i}.root' for i in range(0,79))

    folders = [
        # "/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/anayak/2022NanoAOD/Muon_Fill8102/Run356943/",
        # "/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/anayak/2022NanoAOD/Muon_Fill8102/Run356944/",
        # "/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/anayak/2022NanoAOD/Muon_Fill8102/Run356945/",
        # "/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/anayak/2022NanoAOD/Muon_Fill8102/Run356946/",
        # "/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/anayak/2022NanoAOD/Muon_Fill8102/Run356947/",
        # "/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/anayak/2022NanoAOD/Muon_Fill8102/Run356948/",
        # "/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/anayak/2022NanoAOD/Muon_Fill8102/Run356949/",
        # "/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/anayak/2022NanoAOD/Muon_Fill8102/Run356951/",
        # "/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/anayak/2022NanoAOD/Muon_Fill8102/Run356954/",
        # "/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/anayak/2022NanoAOD/Muon_Fill8102/Run356955/",
        # "/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/anayak/2022NanoAOD/Muon_Fill8102/Run356956/",
        "/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/savarghe/nanoaod/eraD/Fill8136/Muon/"
    ]

    df = create_rdataframe(folders)
    h_num_os, h_den_os = obtain_histograms(df, channel, iseta, plottingVariable)
    plot(h_num_os, h_den_os, plottingVariable, channnel, args.run, args.plot)