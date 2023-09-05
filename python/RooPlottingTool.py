import numpy as np
import ROOT
from array import array

def CreateBins(is_eta, is_jet=False):
    if is_eta:
        return np.arange(-2.5,3.5,1.0)
    elif not is_jet:
        bins = np.arange(20, 40, step=4)
        bins = np.append(bins, np.arange(40, 60, step=10))
        #bins = np.append(bins, np.arange(60, 100, step=10))
        high_pt_bins = [ 60, 150, 200]
    else:
        bins = np.arange(20, 40, step=10)
        bins = np.append(bins, np.arange(40, 120, step=4))
        #bins = np.append(bins, np.arange(60, 100, step=10))
        high_pt_bins = [ 120, 150, 200]
    return np.append(bins,high_pt_bins)


def CreateHistModel(histname,is_eta, is_jet=False):
    bins = CreateBins(is_eta, is_jet)
    hist_model = ROOT.RDF.TH1DModel(histname,"", len(bins) - 1, array('d', bins))
    return hist_model

