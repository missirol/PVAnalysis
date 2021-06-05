#!/usr/bin/env python
import ROOT

def print_pvOutput(filename, pvColl='offlinePrimaryVertices'):

  aTFile = ROOT.TFile.Open(filename)
  if (not aTFile) or aTFile.IsZombie():
    raise RuntimeError(filename)

  vals = { 'numEvents': None }

  for _tmp in [
    'effvsnsimevtSignal',
    'eff4vsnsimevtSignal',
    'effselvsnsimevtSignal',
  ]:
    tmp_prof = aTFile.Get(pvColl+'/'+_tmp)
    if not tmp_prof:
      raise RuntimeError(pvColl+'/'+_tmp)

    if vals['numEvents'] is None:
       vals['numEvents'] = tmp_prof.GetEntries()

    tmp_num, tmp_den = 0., 0.
    for idx in range(tmp_prof.GetNbinsX()+2):
      tmp_den += tmp_prof.GetBinEntries(idx)
      tmp_num += tmp_prof.GetBinEntries(idx) * tmp_prof.GetBinContent(idx)

    if vals['numEvents'] != tmp_den:
      raise RuntimeError(_tmp)

    vals[_tmp+'_num'] = tmp_num
    vals[_tmp+'_den'] = tmp_den

    print ' {:40} ({:5.1f} / {:5.1f}) = {:5.6f}'.format(_tmp, tmp_num, tmp_den, tmp_num/tmp_den)

  h_matchedsignalvtxsel_index = aTFile.Get(pvColl+'/matchedsignalvtxsel/index')
  evtSigVtxMatchedTo1stRecoVtx = h_matchedsignalvtxsel_index.GetBinContent(1)
  evtSigVtxMatchedToOneRecoVtx = h_matchedsignalvtxsel_index.Integral()

  print ' --> index(0) =', evtSigVtxMatchedTo1stRecoVtx, '(of', evtSigVtxMatchedToOneRecoVtx, ') -->', evtSigVtxMatchedTo1stRecoVtx/evtSigVtxMatchedToOneRecoVtx

  aTFile.Close()
