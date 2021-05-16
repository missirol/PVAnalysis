#!/usr/bin/env python
import os
import sys
import argparse
import ROOT
import math

from usercode.PrimaryVertexAnalyzer.utils.common import *
from usercode.PrimaryVertexAnalyzer.utils.th1 import *
from usercode.PrimaryVertexAnalyzer.utils.efficiency import *
from usercode.PrimaryVertexAnalyzer.utils.plot import *
from usercode.PrimaryVertexAnalyzer.utils.plot_style import *

COUNTER = 0
def tmpName(increment=True):
  global COUNTER
  COUNTER += 1
  return 'tmp'+str(COUNTER)

def getHistogram(tfile, key):
  h0 = tfile.Get(key)
  if not h0: return None

  hret = h0.Clone()
  hret.SetDirectory(0)
  hret.UseCurrentStyle()

  return hret

def print_pvEfficiencies(**kwargs):
  filename = kwargs['filename']
  pvColl = kwargs['pvColl']

  outLines = [
    '-'*100,
    filename[-20:-10]+' '+pvColl,
  ]

  aTFile = ROOT.TFile.Open(filename)
  if (not aTFile) or aTFile.IsZombie():
    raise RuntimeError(filename)

  h_nsimvtx = aTFile.Get('simpvs/nsimvtx')
  totEvents = h_nsimvtx.GetEntries()

  h_xsim = aTFile.Get('simpvs/xsim')
  nSimVtxs = h_xsim.GetEntries()

  h_matchedvtxsel_index = aTFile.Get(pvColl+'/matchedvtxsel/index')
  nRecoVtxsMatched = h_matchedvtxsel_index.GetEntries()

  h_matchedsignalvtxsel_index = aTFile.Get(pvColl+'/matchedsignalvtxsel/index')
  nRecoVtxsMatchedSignal = h_matchedsignalvtxsel_index.GetEntries()
  nRecoVtxsMatchedSignalIdx0 = h_matchedsignalvtxsel_index.GetBinContent(1)

  # pct of reco-vtxs matched to a sim-vtx
  effRecoMatched = get_efficiency_f(nRecoVtxsMatched, nSimVtxs)

  outLines += ['{:<60} = {:5.6f} +{:5.6f} -{:5.6f}'.format(
    '% of reco-vtxs matched to a sim-vtx',
    effRecoMatched[0],
    effRecoMatched[1],
    effRecoMatched[2]
  )]

#  # pct of reco-vtxs matched to signal sim-vtx
#  effRecoMatchedSignal = get_efficiency_f(nRecoVtxsMatchedSignal, nSimVtxs)
#
#  outLines += ['{:<60} = {:5.6f} +{:5.6f} -{:5.6f}'.format(
#    '% of reco-vtxs matched to signal sim-vtx',
#    effRecoMatchedSignal[0],
#    effRecoMatchedSignal[1],
#    effRecoMatchedSignal[2]
#  )]

  # pct of events with 1st reco-vtxs matched to signal sim-vtx
  effRecoMatchedSignalIdx0 = get_efficiency_f(nRecoVtxsMatchedSignalIdx0, nSimVtxs)

  outLines += ['{:<60} = {:5.6f} +{:5.6f} -{:5.6f}'.format(
    '% of events with 1st reco-vtxs matched to signal sim-vtx',
    effRecoMatchedSignalIdx0[0],
    effRecoMatchedSignalIdx0[1],
    effRecoMatchedSignalIdx0[2]
  )]

  # mean number of fake vertices (not matched to a sim-vtx)
  p_ntpfakeselvssimPU = aTFile.Get(pvColl+'/ntpfakeselvssimPU')
  meanNum_ntpfakesel_num = 0.
  meanNum_ntpfakesel_den = 0.
  for idx in range(p_ntpfakeselvssimPU.GetNbinsX()+2):
    meanNum_ntpfakesel_den += p_ntpfakeselvssimPU.GetBinEntries(idx)
    meanNum_ntpfakesel_num += p_ntpfakeselvssimPU.GetBinEntries(idx) * p_ntpfakeselvssimPU.GetBinContent(idx)
  meanNum_ntpfakesel = meanNum_ntpfakesel_num / meanNum_ntpfakesel_den

  outLines += ['{:<60} = {:5.6f}'.format(
    'mean number of fake vertices (not matched to a sim-vtx)', meanNum_ntpfakesel)
  ]

  aTFile.Close()

  for _tmp in outLines:
    print _tmp

def plot_pvResolutions(**kwargs):
  inputDatasets = kwargs['inputDatasets']
  outputName = kwargs['outputName']
  exts = kwargs['exts']
  labelTopLeftOut = kwargs.get('labelTopLeftOut', '')
  labelTopLeftIn = kwargs.get('labelTopLeftIn', '')
  labelTopRightOut = kwargs.get('labelTopRightOut', '')
  labelTopRightIn = kwargs.get('labelTopRightIn', '')

  resolution_keys = [
    'matchedvtxsel/xrecsim',
    'matchedvtxsel/yrecsim',
    'matchedvtxsel/zrecsim',
    'matchedvtxsel/zrecsimHR',
    'matchedvtxsel/xrecsimpull',
    'matchedvtxsel/yrecsimpull',
    'matchedvtxsel/zrecsimpull',
  ]

  inputDatasets_names = [_tmp['name'] for _tmp in inputDatasets]

  histos = {}
  for _tmp in inputDatasets:
    _tmpTFile = ROOT.TFile.Open(_tmp['file'])
    if not _tmpTFile:
      WARNING('failed to open target TFile: '+_tmp['file'])
      continue

    for _tmpKey in resolution_keys:
      if _tmpKey not in histos: histos[_tmpKey] = {}

      histos[_tmpKey][_tmp['name']] = getHistogram(_tmpTFile, _tmp['TKeyPrefix']+'/'+_tmpKey)
      if histos[_tmpKey][_tmp['name']] is not None:
        histos[_tmpKey][_tmp['name']].Scale(1./histos[_tmpKey][_tmp['name']].Integral())

  for _tmpKey in histos:
    if   _tmpKey == 'matchedvtxsel/xrecsim': xtitle = 'x_{reco} - x_{sim} [cm]'
    elif _tmpKey == 'matchedvtxsel/yrecsim': xtitle = 'y_{reco} - y_{sim} [cm]'
    elif _tmpKey == 'matchedvtxsel/zrecsim': xtitle = 'z_{reco} - z_{sim} [cm]'
    elif _tmpKey == 'matchedvtxsel/zrecsimHR': xtitle = 'z_{reco} - z_{sim} [cm]'
    elif _tmpKey == 'matchedvtxsel/xrecsimpull': xtitle = '(x_{reco} - x_{sim})/#sigma^{x}_{reco}'
    elif _tmpKey == 'matchedvtxsel/yrecsimpull': xtitle = '(y_{reco} - y_{sim})/#sigma^{y}_{reco}'
    elif _tmpKey == 'matchedvtxsel/zrecsimpull': xtitle = '(z_{reco} - z_{sim})/#sigma^{z}_{reco}'

    _tmpKeyOutput = _tmpKey.replace('/', '_')
    _outputWoExt = outputName+'_'+_tmpKeyOutput
    _canvasName = os.path.basename(_outputWoExt)

    canvas = ROOT.TCanvas(_canvasName, _canvasName)
    canvas.cd()

    if _tmpKey.endswith('pull'):
      h0 = canvas.DrawFrame(-3., 0.0001, 3., 0.12)
    elif _tmpKey.endswith('xrecsim') or _tmpKey.endswith('yrecsim'):
      h0 = canvas.DrawFrame(-0.002, 0.0001, 0.002, 0.4)
    else:
      h0 = canvas.DrawFrame(-0.005, 0.0001, 0.005, 0.2)

    hgroup = histos[_tmpKey]

    for _tmpDset in inputDatasets:
      hgroup[_tmpDset['name']].SetMarkerStyle(20)
      hgroup[_tmpDset['name']].SetMarkerSize(.0)
      hgroup[_tmpDset['name']].SetLineWidth(2)
      hgroup[_tmpDset['name']].SetLineStyle(1)
      hgroup[_tmpDset['name']].SetLineColor(_tmpDset['color'])
      hgroup[_tmpDset['name']].SetMarkerColor(_tmpDset['color'])
      hgroup[_tmpDset['name']].Draw('hist,e0,same')

    topLabel = ROOT.TPaveText(0.165, 0.85, 0.65, 0.90, 'NDC')
    topLabel.SetFillColor(0)
    topLabel.SetFillStyle(1001)
    topLabel.SetTextColor(ROOT.kBlack)
    topLabel.SetTextAlign(12)
    topLabel.SetTextFont(42)
    topLabel.SetTextSize(0.035)
    topLabel.SetBorderSize(0)
    topLabel.AddText(labelTopLeftIn)
    topLabel.Draw('same')

    objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
    objLabel.SetFillColor(0)
    objLabel.SetFillStyle(1001)
    objLabel.SetTextColor(ROOT.kBlack)
    objLabel.SetTextAlign(32)
    objLabel.SetTextFont(42)
    objLabel.SetTextSize(0.035)
    objLabel.SetBorderSize(0)
    objLabel.AddText(labelTopRightOut)
    objLabel.Draw('same')

    l1tRateLabel = ROOT.TPaveText(0.165, 0.79, 0.45, 0.84, 'NDC')
    l1tRateLabel.SetFillColor(0)
    l1tRateLabel.SetFillStyle(1001)
    l1tRateLabel.SetTextColor(ROOT.kBlack)
    l1tRateLabel.SetTextAlign(12)
    l1tRateLabel.SetTextFont(42)
    l1tRateLabel.SetTextSize(0.035)
    l1tRateLabel.SetBorderSize(0)
#    l1tRateLabel.AddText(labelTopLeftIn)
#    l1tRateLabel.Draw('same')

    hltRateLabel = ROOT.TPaveText(0.165, 0.74, 0.45, 0.79, 'NDC')
    hltRateLabel.SetFillColor(0)
    hltRateLabel.SetFillStyle(1001)
    hltRateLabel.SetTextColor(ROOT.kBlack)
    hltRateLabel.SetTextAlign(12)
    hltRateLabel.SetTextFont(42)
    hltRateLabel.SetTextSize(0.035)
    hltRateLabel.SetBorderSize(0)
    hltRateLabel.AddText('')
#    hltRateLabel.Draw('same')

    genJetPtLabel = ROOT.TPaveText(0.65, 0.80, 0.94, 0.90, 'NDC')
    genJetPtLabel.SetFillColor(0)
    genJetPtLabel.SetFillStyle(1001)
    genJetPtLabel.SetTextColor(ROOT.kBlack)
    genJetPtLabel.SetTextAlign(22)
    genJetPtLabel.SetTextFont(42)
    genJetPtLabel.SetTextSize(0.035)
    genJetPtLabel.SetBorderSize(0)
    genJetPtLabel.AddText(labelTopRightIn)
#    genJetPtLabel.Draw('same')

    leg1 = ROOT.TLegend(0.75, 0.60, 0.94, 0.90)
    leg1.SetNColumns(1)
    leg1.SetTextFont(42)
    leg1.SetTextSize(0.035)
    for _tmpDset in inputDatasets:
      leg1.AddEntry(
        hgroup[_tmpDset['name']],
        _tmpDset['name'], #+' #scale[0.8]{(RMS = '+'{:1.5f}'.format(hgroup[_tmpDset['name']].GetRMS() * 1e4)+'#mum)}',
        'lex',
      )
    leg1.Draw('same')

    h0.SetTitle(';'+xtitle+';a.u.')
    h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

    if _tmpKey.endswith('xrecsim') or _tmpKey.endswith('yrecsim') or _tmpKey.endswith('zrecsimHR'):
      h0.GetXaxis().SetNdivisions(505)

    canvas.SetLogy(0)
    canvas.SetGrid(1, 1)
    canvas.Update()

    for _tmpExt in exts:
      canvas.SaveAs(outputName+'_'+_tmpKeyOutput+'.'+_tmpExt)

    canvas.Close()

    print '\033[1m'+os.path.relpath(_outputWoExt, os.environ['PWD'])+'\033[0m'

#### main
if __name__ == '__main__':
  ### args ---------------
  parser = argparse.ArgumentParser(description=__doc__)

  parser.add_argument('-i', '--input', dest='inputDir', action='store', default=None, required=True,
                      help='path to input harvesting/ directory')

  parser.add_argument('-o', '--output', dest='outputDir', action='store', default=None, required=True,
                      help='path to output directory')

  parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['pdf', 'png'],
                      help='list of extension(s) for output file(s)')

  parser.add_argument('-v', '--verbosity', dest='verbosity', nargs='?', const=1, type=int, default=0,
                      help='verbosity level')

  parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                      help='enable dry-run mode')

  opts, opts_unknown = parser.parse_known_args()
  ### --------------------

  log_prx = os.path.basename(__file__)+' -- '

  ROOT.gROOT.SetBatch() # disable interactive graphics
  ROOT.gErrorIgnoreLevel = ROOT.kError # do not display ROOT warnings

#  ROOT.TH1.AddDirectory(False)

  theStyle = get_style(0)
  theStyle.cd()

  EXTS = list(set(opts.exts))

  ### args validation ---
  inputDir = os.path.abspath(opts.inputDir)

  outputDir = os.path.abspath(opts.outputDir)
  MKDIRP(outputDir, verbose = (opts.verbosity > 0), dry_run = opts.dry_run)

  for pvColl in [
    'offlinePrimaryVertices',
    'offlinePrimaryVerticesWithBS',
  ]:
    for _tmpf in [
      '/Phase2_D76/RelValTenMuExtendedE0To200_mcRun4_D76_NoPU.root',
      '/Phase2_D78/RelValTenMuExtendedE0To200_mcRun4_D78_NoPU.root',
      '/Phase2_D80/RelValTenMuExtendedE0To200_mcRun4_D80_NoPU.root',
      '/Phase2_D81/RelValTenMuExtendedE0To200_mcRun4_D81_NoPU.root',
    ]:
      print_pvEfficiencies(**{'filename': inputDir+_tmpf, 'pvColl': pvColl})

    plot_pvResolutions(
      inputDatasets = [
        {'name': 'T21',
         'file': inputDir+'/Phase2_D76/RelValTenMuExtendedE0To200_mcRun4_D76_NoPU.root',
         'TKeyPrefix': pvColl,
         'color': ROOT.kBlack,
        },
        {'name': 'T22',
         'file': inputDir+'/Phase2_D78/RelValTenMuExtendedE0To200_mcRun4_D78_NoPU.root',
         'TKeyPrefix': pvColl,
         'color': ROOT.kRed,
        },
        {'name': 'T25',
         'file': inputDir+'/Phase2_D80/RelValTenMuExtendedE0To200_mcRun4_D80_NoPU.root',
         'TKeyPrefix': pvColl,
         'color': ROOT.kBlue,
        },
        {'name': 'T26',
         'file': inputDir+'/Phase2_D81/RelValTenMuExtendedE0To200_mcRun4_D81_NoPU.root',
         'TKeyPrefix': pvColl,
         'color': ROOT.kViolet,
        },
      ],
      labelTopLeftIn = pvColl,
      labelTopRightOut = 'Phase-2, NoPU (14 TeV)',
      outputName = outputDir+'/'+pvColl,
      exts = EXTS,
    )
