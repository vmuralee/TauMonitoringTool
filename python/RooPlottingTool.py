import numpy as np
import ROOT
from array import array

def CreateBins(is_eta):
    if is_eta:
        return np.arange(-3,3,0.5)
    else:
        bins = np.arange(20, 40, step=4)
        bins = np.append(bins, np.arange(40, 60, step=10))
        #bins = np.append(bins, np.arange(60, 100, step=10))
        high_pt_bins = [ 60, 150, 200]
    return np.append(bins,high_pt_bins)


def CreateHistModel(histname,is_eta):
    bins = CreateBins(is_eta)
    hist_model = ROOT.RDF.TH1DModel(histname,"", len(bins) - 1, array('d', bins))
    return hist_model
