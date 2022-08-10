import os
import sys

import ROOT

# Enable multi-threading                                                                                                                                                                                    
ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True)


import argparse

parser = argparse.ArgumentParser(description='Skim full tuple.')
parser.add_argument('--input', required=False, type=str, nargs='+', help="input files")
parser.add_argument('--channel', required=True, type=str, help="ditau,mutau or etau")
parser.add_argument('--run', required=True, type=str, help="tau selection")
parser.add_argument('--plot', required=True, type=str, help="plot name")
parser.add_argument('--iseta',action='store_true', help="plot name")
parser.add_argument('--var', required=True, type=str, help="tau_pt or tau_eta")

args = parser.parse_args()



core_dir = str(os.getcwd()).split('producer')

Trigger_header_path = os.path.join(core_dir[0] +'/interface' + os.sep,"picoNtupler.h")

ROOT.gInterpreter.Declare('#include "{}"'.format(Trigger_header_path))

sys.path.insert(1, core_dir[0]+'/python')
from RooPlottingTool import *


inputFiles = (f'/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/anayak/2022NanoAOD/SingleMuonV1/Files2/nano_aod_{i}.root' for i in range(0,79))


df = ROOT.RDataFrame("Events",inputFiles)

# Tag And Probe selection {Obtaining high pure Z -> mu tau Events}

## select muon (Tag) candidate 

df_tag = df.Filter("nMuon == 1 && nTau >=1").Define("Muon_Index","MuonIndex(nTrigObj,TrigObj_id,TrigObj_filterBits,TrigObj_pt,TrigObj_eta,TrigObj_phi,nMuon,Muon_pt,Muon_eta,Muon_phi,Muon_mass,Muon_pfRelIso04_all)").Define("muon_p4","Muon_p4(Muon_Index,Muon_pt,Muon_eta,Muon_phi,Muon_mass)")

## select tau (probe) candidate

df_probe = df_tag.Filter("Muon_Index >= 0").Define("Tau_Index","TauIndex(nTau,Tau_pt,Tau_eta,Tau_phi,Tau_mass,Tau_dz,muon_p4)")

df_probe_id = df_probe.Filter("Tau_Index >= 0 && Tau_idDeepTau2017v2p1VSjet[Tau_Index] >=16 && Tau_idDeepTau2017v2p1VSmu[Tau_Index] >=8 && Tau_idDeepTau2017v2p1VSe[Tau_Index] >=2").Define("tau_p4","Tau_p4(Tau_Index,Tau_pt,Tau_eta,Tau_phi,Tau_mass)")

## select mu-tau pair with os and ss events
df_TandP_os = df_probe_id.Define('weight',"(Tau_charge[Tau_Index] != Muon_charge[Tau_Index]) ? 1. : -1.").Define("mT","CalcMT(muon_p4,MET_pt,MET_phi)").Define("m_vis","ZMass(tau_p4,muon_p4)")

## select pure Z -> mu tau events
df_TandP = df_TandP_os.Filter("mT < 30 && m_vis > 40 && m_vis < 80").Define("tau_pt","Tau_pt[Tau_Index]").Define("tau_eta","Tau_eta[Tau_Index]")

#print(ss_events,"   ",os_events)

# Calculate Efficiency 
h_num_os = df_TandP.Histo1D(CreateHistModel("numerator",args.iseta),args.var)
h_den_os = df_TandP.Histo1D(CreateHistModel("denominator",args.iseta),args.var)


#h_den_os.Add(h_den_ss.GetPtr(),-1)


if(args.channel == 'ditau'):
    df_TandP_num = df_TandP.Define("pass_ditau","PassDiTauFilter(nTrigObj,TrigObj_id,TrigObj_filterBits,TrigObj_pt,TrigObj_eta,TrigObj_phi,Tau_pt[Tau_Index],Tau_eta[Tau_Index],Tau_phi[Tau_Index])")
    h_num_os = df_TandP_num.Filter("pass_ditau > 0.5 && HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1 == 1").Histo1D(CreateHistModel("numerator",args.iseta),args.var,'weight')
elif(args.channel == 'mutau'):
    df_TandP_num = df_TandP.Define("pass_mutau","PassMuTauFilter(nTrigObj,TrigObj_id,TrigObj_filterBits,TrigObj_pt,TrigObj_eta,TrigObj_phi,Tau_pt[Tau_Index],Tau_eta[Tau_Index],Tau_phi[Tau_Index])")
    h_num_os = df_TandP_num.Filter("pass_mutau > 0.5 && HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1==1").Histo1D(CreateHistModel("numerator",args.iseta),args.var,'weight')
    
#h_num_os.Add(h_num_ss.GetPtr(),-1)

## Produce plot                 
print("Create TurnON")                                                                                                                                                                         
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c = ROOT.TCanvas("c", "", 800, 700)
gr = ROOT.TEfficiency(h_num_os.GetPtr(),h_den_os.GetPtr())
gr.SetTitle("")
gr.Draw()
label = ROOT.TLatex(); label.SetNDC(True)
if(args.var == "tau_pt" or args.var=="tau_l1pt"):
    label.DrawLatex(0.8, 0.03, "#tau_pT")
else:
    label.DrawLatex(0.8, 0.03, "#eta_#tau")
label.SetTextSize(0.040); label.DrawLatex(0.100, 0.920, "#bf{CMS Run3 Data}")
label.SetTextSize(0.030); label.DrawLatex(0.630, 0.920, "#sqrt{s} = 13.6 TeV, "+args.run)

c.SaveAs(args.plot+".pdf")

