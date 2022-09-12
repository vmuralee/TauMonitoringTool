from picoNtupler_TandP import *

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

plotname = "testplot"
label = "Fill 8136"

df = create_rdataframe(folders)

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