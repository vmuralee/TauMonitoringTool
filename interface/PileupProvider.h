#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
 

#pragma once


class PileUpWeightProvider {
 public:
  PileUpWeightProvider(const TH1D& data_pu_orig, const TH1D& mc_pu_orig)
    {
      TH1D data_pu(data_pu_orig);
      data_pu.Scale(1. / data_pu.Integral());
      TH1D mc_pu(mc_pu_orig);
      mc_pu.Scale(1. / mc_pu.Integral());
      ratio.reset(new TH1D(data_pu));
      ratio->Divide(&mc_pu);
    }

  float GetWeight(int npu) const
  {
    int bin = ratio->FindBin(npu);
    if(bin < 1 || bin > ratio->GetNbinsX())
      return 0;
    return ratio->GetBinContent(bin);
  }

  static void Initialize(const TH1D& data_pu, const TH1D& mc_pu)
  {
    default_provider.reset(new PileUpWeightProvider(data_pu, mc_pu));
  }

  static const PileUpWeightProvider& GetDefault()
  {
    if(!default_provider)
      throw std::runtime_error("Default PileUpWeightProvider is not initialized.");
    return *default_provider;
  }

 private:
  static std::unique_ptr<PileUpWeightProvider> default_provider;

 private:
  std::unique_ptr<TH1D> ratio;
};

std::unique_ptr<PileUpWeightProvider> PileUpWeightProvider::default_provider;
