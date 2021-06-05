### Tools for analysis of primary-vertex reconstruction

* [Setup](#setup)
* [Configuration files](#configuration-files)
* [Batch processing at PSI's Tier-3](#batch-processing-at-psis-tier-3)
* [Additional Notes](#additional-notes)

----------

#### Setup
```shell
voms-proxy-init -voms cms -rfc -valid 168:00

scram p -n CMSSW_11_3_0_pre6 CMSSW CMSSW_11_3_0_pre6
cd CMSSW_11_3_0_pre6/src
eval `scram runtime -sh`

git clone https://github.com/missirol/PVAnalysis.git usercode -o missirol -b devel3

scram b -j 8
```

#### Configuration files

The directory `${CMSSW_BASE}/src/usercode/PrimaryVertexAnalyzer/test`
contains a set of `cmsRun` configuration files,
corresponding to different types of PV-related analyses.

An example of how to run a test with one of these cfg files is given below:
```shell
cmsRun ${CMSSW_BASE}/src/usercode/PrimaryVertexAnalyzer/test/cfg/pva_cfg.py \
  dumpPython=pva_configDump.py maxEvents=10 reco=Phase2_D76 output=tmp_Phase2_D76.root
```

#### Batch processing at PSI's Tier-3

Submission of multiple jobs to a batch system can be done using
the executables `scripts/bdriver` and `scripts/bmonitor`.

The first one creates the output directory structure
and the executables to be used by the batch jobs,
while the second one allows to monitor and
manage (e.g. resubmit) the jobs themselves.

For a given set of jobs, one runs the `bdriver` step first (and only once),
and then controls the jobs running `bmonitor` as many times as needed,
until all jobs complete successfully.

*NB* --
Both scripts support two batch systems:
`HTCondor` (in use on `lxplus` machines), and `SLURM` (in use at `T3_PSI_CH`);
the `HTCondor` functionalities are expected to work,
but they are currently under-tested,
as the development is mainly done at `T3_PSI_CH`.

The commands below show an example of this type of workflow;
in this example, the script `test/prod/bjobs_Phase2_trkGeomsSensorTF_210514.sh`
serves as a wrapper calling `bdriver` for a certain group of DAS samples.
Such a wrapper represents a "production",
i.e. the execution of a given analysis (i.e. cfg file + cmd-line args)
on a list of input data sets.
Typically, for a new "production" of results the user would write
a new wrapper under `prod/` specifying the relevant input data sets
and configuration file (+ its command-line arguments).
```shell
# path to output directory on T3 Storage Element (SE)
outdir=/pnfs/psi.ch/cms/trivcat/store/user/${USER}/test/pvtx/prod/$(date +%y%m%d)_prodTag

# wrapper to create scripts for cmsRun jobs to be submitted to the SLURM batch system
${CMSSW_BASE}/src/usercode/PrimaryVertexAnalyzer/test/prod/bjobs_Phase2_trkGeomsSensorTF_210514.sh ${outdir}

# run one job locally
SLURM_ARRAY_TASK_ID=6 $(ls -1 ${outdir}/*/*/slurm_exe.sh | head -1)

# check status of all the tasks prepared by the driver
bmonitor -i ${outdir}

# submit a max of 100 jobs via SLURM
bmonitor -i ${outdir} -r -m 100
```

#### Additional Notes

 * [CMSWeb Portal](https://cmsweb.cern.ch) (contains links to DAS, DQMs, etc)

 * [CMS Data Aggregation System (DAS)](https://cmsweb.cern.ch/das)

 * CMS Production Monitoring (CMSProdMon): [all active campaigns in production](https://dmytro.web.cern.ch/dmytro/cmsprodmon/status.php)
