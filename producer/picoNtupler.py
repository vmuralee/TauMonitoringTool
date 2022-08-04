import argparse
import ROOT
import os 
import sys 

# Enable multi-threading
ROOT.ROOT.EnableImplicitMT()


parser = argparse.ArgumentParser(description='Skim full tuple.')
parser.add_argument('--input', required=False, type=str, nargs='+', help="input files")
parser.add_argument('--channel', required=True, type=str, help="ditau,mutau or etau")
parser.add_argument('--run', required=True, type=str, help="tau selection")
parser.add_argument('--plot', required=True, type=str, help="plot name")

args = parser.parse_args()



core_dir = str(os.getcwd()).split('producer')

Trigger_header_path = os.path.join(core_dir[0] +'interface' + os.sep,"picoNtupler.h")

ROOT.gInterpreter.Declare('#include "{}"'.format(Trigger_header_path))

sys.path.insert(1, core_dir[0]+'/python')
from RooPlottingTool import *



inputFiles = (f'/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/anayak/2022NanoAOD/SingleMuonV1/Files2/nano_aod_{i}.root' for i in range(0,79))


df = ROOT.RDataFrame("Events",inputFiles)

# select tag events

df_tag = df.Filter("nMuon >= 1 && nTau >=1").Define("Muon_Index","MuonIndex(nTrigObj,TrigObj_id,TrigObj_filterBits,TrigObj_pt,TrigObj_eta,TrigObj_phi,nMuon,Muon_pt,Muon_eta,Muon_phi,Muon_mass,Muon_pfRelIso04_all)")
# select muon+tau pair


df_mutau =  df_tag.Filter("Muon_Index >= 0").Define("Tau_Index","TauIndex(nTau,Tau_pt,Tau_eta,Tau_phi,Tau_mass,Tau_dz,nMuon,Muon_Index,Muon_pt,Muon_eta,Muon_phi,Muon_mass)")
# select taus with DeepTauID 


pass_ditau = "PassDiTauFilter(nTrigObj,TrigObj_id,TrigObj_filterBits,TrigObj_pt,TrigObj_eta,TrigObj_phi,Tau_pt[Tau_Index],Tau_eta[Tau_Index],Tau_phi[Tau_Index]) > 0 && Tau_Index >= 0"
pass_mutau = "PassMuTauFilter(nTrigObj,TrigObj_id,TrigObj_filterBits,TrigObj_pt,TrigObj_eta,TrigObj_phi,Tau_pt[Tau_Index],Tau_eta[Tau_Index],Tau_phi[Tau_Index]) > 0 && Tau_Index >= 0"
pass_eltau = "PassElTauFilter(nTrigObj,TrigObj_id,TrigObj_filterBits,TrigObj_pt,TrigObj_eta,TrigObj_phi,TrigObj_l1pt,TrigObj_l1iso,Tau_pt[Tau_Index],Tau_eta[Tau_Index],Tau_phi[Tau_Index]) > 0 && Tau_Index >= 0"

pass_probe = pass_ditau
if(args.channel == 'ditau'):
    pass_probe = pass_ditau
elif(args.channel == 'mutau'):
    pass_probe = pass_mutau
elif(args.channel == 'etau'):
    pass_probe = pass_eltau
else:
    print("Write proper channel")

tau_id   = "Tau_idDeepTau2017v2p1VSjet[0] >=16 && Tau_idDeepTau2017v2p1VSmu[0] >=8 && Tau_idDeepTau2017v2p1VSe[0] >=2"

df_mutau_final = df_mutau.Filter("Tau_charge[Tau_Index] != Muon_charge[Tau_Index]").Define("tau_p4","Tau_p4(Tau_Index,Tau_pt,Tau_eta,Tau_phi,Tau_mass)").Define("muon_p4","Muon_p4(Muon_Index,Muon_pt,Muon_eta,Muon_phi,Muon_mass)").Define("btag_veto","PassBtagVeto(muon_p4,tau_p4,nJet,Jet_pt,Jet_eta,Jet_phi,Jet_mass,Jet_btagCSVV2)")

df_pass= df_mutau_final.Filter(pass_probe+" && "+tau_id+" && btag_veto > 0.5").Define("tau_pt","LeadingTauPT(Tau_pt,Tau_eta,Tau_phi,Tau_mass,Tau_Index)")
df_all = df_mutau_final.Filter(tau_id+" && btag_veto > 0.5").Define("tau_pt","LeadingTauPT(Tau_pt,Tau_eta,Tau_phi,Tau_mass,Tau_Index)")

df_pass_var = df_pass.Define("tau_eta","LeadingTauEta(Tau_pt,Tau_eta,Tau_phi,Tau_mass,Tau_Index)")
df_all_var  = df_all.Define("tau_eta","LeadingTauEta(Tau_pt,Tau_eta,Tau_phi,Tau_mass,Tau_Index)")


def CreateTurnOn(var_name,df_pass_var,df_all_var,is_eta,plotname):

    h_num = df_pass_var.Filter("tau_eta != -999").Histo1D(CreateHistModel("probe_tau",is_eta),var_name)
    h_den = df_all_var.Filter("tau_eta != -999").Histo1D(CreateHistModel("all_tau",is_eta),var_name)

    # Produce plot
    ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
    c = ROOT.TCanvas("c", "", 800, 700)


    gr = ROOT.TEfficiency(h_num.GetPtr(),h_den.GetPtr()) 
    gr.SetTitle("")
    
    gr.Draw()
    
    label = ROOT.TLatex(); label.SetNDC(True)
    if(var_name == "tau_pt"):
        label.DrawLatex(0.8, 0.03, "#tau_pT")
    else:
        label.DrawLatex(0.8, 0.03, "#eta_#tau")
    label.SetTextSize(0.040); label.DrawLatex(0.100, 0.920, "#bf{CMS Run3 Data}")
    label.SetTextSize(0.030); label.DrawLatex(0.630, 0.920, "#sqrt{s} = 13.6 TeV, "+args.run)
 
    c.SaveAs(plotname+".pdf")
    c.Delete 

print("Creating TurnOn pT")
CreateTurnOn("tau_pt",df_pass_var,df_all_var,False,args.plot)
# print("Creating TurnOn Eta")
# CreateTurnOn("tau_eta",df_pass_var,df_all_var,True,"MuTau_eta")
