###
### command-line arguments
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('skipEvents', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of events to be skipped')

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to python file with content of cms.Process')

opts.register('numThreads', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of threads')

opts.register('numStreams', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of streams')

opts.register('lumis', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to .json with list of luminosity sections')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('pruneProcess', True,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'prune content of cms.Process')

opts.register('globalTag', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag')

opts.register('reco', '',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword to select base configuration file')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'level of output verbosity')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.parseArguments()

###
### GlobalTag
###
if opts.globalTag is not None:
  from Configuration.AlCa.GlobalTag import GlobalTag
  process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')

###
### base configuration file
###
if opts.reco == 'Phase2_D76':
  cmsDriverCmd = """cmsDriver.py step3\
 --conditions auto:phase2_realistic_T21\
 --era Phase2C11I13M9\
 --geometry Extended2026D76\
 --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000\
 --step RECO\
 --processName RERECO\
 --number 10\
 --filein /store/relval/CMSSW_11_3_0_pre6/RelValTenMuExtendedE_0_200/GEN-SIM-RECO/113X_mcRun4_realistic_v6_2026D76noPU-v1/10000/44134f9e-3ebc-4e59-942a-44131f79f61c.root\
 --no_exec\
"""

elif opts.reco == 'Phase2_D78':
  cmsDriverCmd = """cmsDriver.py step3\
 --conditions auto:phase2_realistic_T22\
 --era Phase2C11I13T22M9\
 --geometry Extended2026D78\
 --procModifier PixelCPEGeneric\
 --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000\
 --step RECO\
 --processName RERECO\
 --number 10\
 --filein /store/relval/CMSSW_11_3_0_pre6/RelValTenMuExtendedE_0_200/GEN-SIM-RECO/113X_mcRun4_realistic_v6_2026D78noPU-v1/10000/577041a5-3d32-453c-bc9b-dc530c302ad2.root\
 --no_exec\
"""

else:
  raise RuntimeError('invalid argument for option "reco": "'+opts.reco+'"')

from usercode.PrimaryVertexAnalyzer.utils.common import *
import glob
import os

# create, load and remove the configuration file
EXE(cmsDriverCmd+' --python_filename '+os.path.dirname(__file__)+'/tmp_cfg.py')
from tmp_cfg import cms, process
for _tmpf in glob.glob(os.path.dirname(__file__)+'/tmp_cfg.py*'): os.remove(_tmpf)

# use all input files of the dataset
from usercode.PrimaryVertexAnalyzer.utils.das import *
process.source.fileNames = files_from_dataset(dataset_from_file(process.source.fileNames[0]))

# remove OutputModules of base configuration
for _modname in process.outputModules_():
  _mod = getattr(process, _modname)
  if type(_mod) == cms.OutputModule:
    process.__delattr__(_modname)
    if opts.verbosity > 0:
      print '> removed cms.OutputModule:', _modname

###
### analysis sequence
###
nevent=-1
info = 'test'
debug = False
eventsToProcess = '' #cms.untracked.VEventRange('1:4474')
zdumpcenter = 0
zdumpwidth = 100.
use_tp = True
use_hlt = False
use_2file_solution = False
use_lumiInfo = True

vcollections = ['offlinePrimaryVertices', 'offlinePrimaryVerticesWithBS']

trkTimesLabel = 'tofPID:t0safe'
trkTimeResosLabel = 'tofPID:sigmat0safe'

parameters={  # can be overwritten by arguments of the same name
  '4D': cms.untracked.bool(True),
  'selNdof': cms.untracked.double(4.0),
  'selNdofWithBS': cms.untracked.double(2.0),
#  'splitmethod': cms.untracked.int32(0),
  'usefit': cms.untracked.bool(False),
  'use_tp': cms.untracked.bool(True),
  'use2file': cms.untracked.bool(False),
#  'ptrunc': cms.untracked.double(1.e-50),
  'fill_track_histos': cms.untracked.bool(False),
  'fplo': cms.untracked.double(0),
  'chi2cutoff': cms.double(2.5),
  'verboseAnalyzer': cms.untracked.bool(False),
  'verboseProducer': cms.untracked.bool(False),
  'verboseClusterizer': cms.untracked.bool(False),
  'verboseClusterizer2D': cms.untracked.bool(False),
  'zdumpcenter': cms.untracked.double(0.0),
  'zdumpwidth': cms.untracked.double(20.0),
  'reco': cms.untracked.bool(False),
  'autodump': cms.untracked.int32(0),
  'nDump': cms.untracked.int32(0),
  'nDumpTracks': cms.untracked.int32(0),
#  'mintrkweight': cms.untracked.double(0.5),
  'uniquetrkweight': cms.double(0.8),
  'uniquetrkminp': cms.double(0.0),
  'zmerge': cms.double(1.e-2),
  'coolingFactor': cms.double(0.6),
  'Tmin': cms.double(2.0),
  'Tpurge': cms.double(2.0),
  'Tstop': cms.double(0.5),
  'vertexSize': cms.double(0.006),
  'vertexSizeTime': cms.double(0.008),
  'd0CutOff': cms.double(3.),
  'dzCutOff': cms.double(3.),
  'zrange': cms.double(4),
  'convergence_mode': cms.int32(0),
  'delta_lowT': cms.double(1.e-3),
  'delta_highT': cms.double(1.e-2),
# track selection
  'maxNormalizedChi2': cms.double(10.0),
  'minPixelLayersWithHits': cms.int32(2),
  'minSiliconLayersWithHits': cms.int32(5),
  'maxD0Significance': cms.double(4.0),
  'minPt': cms.double(0.0),
  'maxEta': cms.double(4.0),
  'trackQuality': cms.string('any'),
# track selection, experimental
  'maxDzError': cms.double(1.0),
  'maxD0Error': cms.double(1.0),
# vertex selection
  'minNdof': cms.double(0.0),
# temp
  'trackTimeQualityThreshold': cms.untracked.double(0.8),
  'purge': cms.untracked.int32(0),
  'rho0mode': cms.untracked.int32(0),  # /nt, as before
  'mergenotc': cms.untracked.bool(False),
  'mergeafterpurge': cms.untracked.bool(False),
  'fillzmerge': cms.untracked.double(0.0060), # default = vertexSize
  'use_hitpattern': cms.untracked.int32(0),
  'use_pt': cms.untracked.int32(0)
}

tkFilterParameters = process.unsortedOfflinePrimaryVertices.TkFilterParameters.clone()
print 'original trackFilterParameters (z-clustering)'
print tkFilterParameters
for par_name in [
  'maxNormalizedChi2',
  'minPixelLayersWithHits',
  'minSiliconLayersWithHits',
  'maxD0Significance',
  'maxD0Error',
  'maxDzError',
  'minPt',
  'maxEta',
  'trackQuality',
]:
  try:
    default =  getattr(tkFilterParameters, par_name)
    if default != parameters[par_name]:
      print 'changing tkFilter parameter ', par_name, ' from ', default, '  to ', parameters[par_name]
    setattr(tkFilterParameters, par_name, parameters[par_name])
  except ValueError:
    print 'pvAnalysisOnly_cfg: attribute tkFilterParameters.', par_name , ' not found'

# analysis
process.vertexAnalyzer = cms.EDAnalyzer('PrimaryVertexAnalyzer4PU',
  info = cms.untracked.string(info),
  f4D = parameters['4D'],
  selNdof = parameters['selNdof'],
  selNdofWithBS = parameters['selNdofWithBS'],
  beamSpot = cms.InputTag('offlineBeamSpot'),
  simG4 = cms.InputTag('g4SimHits'),
  outputFile = cms.untracked.string(opts.outputFile),
  verbose = parameters['verboseAnalyzer'],
  veryverbose = cms.untracked.bool(False),
  recoTrackProducer = cms.untracked.string('generalTracks'),
  zmatch = cms.untracked.double(0.05),
  autodump = parameters['autodump'],
  nDump = parameters['nDump'],
  nDumpTracks = parameters['nDumpTracks'],
  RECO = parameters['reco'],
  use_tp = parameters['use_tp'],
  fill_track_histos = parameters['fill_track_histos'],
  track_timing = cms.untracked.bool(True),
  TkFilterParameters = tkFilterParameters,
  trackingParticleCollection = cms.untracked.InputTag('mix', 'MergedTrackTruth'),
  trackingVertexCollection = cms.untracked.InputTag('mix', 'MergedTrackTruth'),
  trackAssociatorMap = cms.untracked.InputTag('trackingParticleRecoTrackAsssociation'),
  TrackTimesLabel = cms.untracked.InputTag(trkTimesLabel),
  TrackTimeResosLabel = cms.untracked.InputTag(trkTimeResosLabel),
#  TrackTimesLabel = cms.untracked.InputTag('tofPID:t0safe'),
#  TrackTimeResosLabel = cms.untracked.InputTag('tofPID:sigmat0safe'),
  TrackTimeQualityMapLabel = cms.untracked.InputTag('mtdTrackQualityMVA:mtdQualMVA'),
  TrackTimeQualityThreshold = cms.untracked.double(parameters['trackTimeQualityThreshold'].value()),
  vertexAssociator = cms.untracked.InputTag('VertexAssociatorByPositionAndTracks'),
  lumiInfoTag = cms.untracked.InputTag('LumiInfo', 'brilcalc'),
  useVertexFilter = cms.untracked.bool(False),
  compareCollections = cms.untracked.int32(0),
  vertexRecoCollections = cms.VInputTag(vcollections),
)

process.setSchedule_(cms.Schedule())

if parameters['use_tp']:
  process.load('Validation.RecoTrack.TrackValidation_cff')
  process.theTruth = cms.Sequence(
      process.tpClusterProducer
    + process.quickTrackAssociatorByHits
    + process.trackingParticleRecoTrackAsssociation
  )
  process.trackingParticleAssociationPath = cms.Path(process.theTruth)
  process.schedule_().append(process.trackingParticleAssociationPath)

process.vertexAnalysisEndPath = cms.EndPath(process.vertexAnalyzer)
process.schedule_().append(process.vertexAnalysisEndPath)

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = max(opts.numThreads, 1)
process.options.numberOfStreams = max(opts.numStreams, 0)

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# select luminosity sections from .json file
if opts.lumis is not None:
  import FWCore.PythonUtilities.LumiList as LumiList
  process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# EDM Input Files
if opts.inputFiles: process.source.fileNames = opts.inputFiles
process.source.secondaryFileNames = opts.secondaryInputFiles if opts.secondaryInputFiles else []

## TFileService
#process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

if opts.pruneProcess:
  process.prune()

# dump content of cms.Process to python file
if opts.dumpPython is not None:
  open(opts.dumpPython, 'w').write(process.dumpPython())
