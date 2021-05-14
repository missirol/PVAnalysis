### Tools for analysis of primary-vertex reconstruction

* [Setup](#setup)
* [Configuration files](#configuration-files)
* [Batch-job workflow at PSI's Tier-3](#batch-job-workflow-at-psi's-tier-3)
* [Additional Notes](#additional-notes)

----------

#### Setup
```
scram p -n CMSSW_11_3_0_pre6 CMSSW CMSSW_11_3_0_pre6
cd CMSSW_11_3_0_pre6/src
eval `scram runtime -sh`
voms-proxy-init -voms cms -rfc -valid 168:00
```

#### Configuration files

The directory `${CMSSW_BASE}/src/usercode/PrimaryVertexAnalyzer/test`
contains a set of `cmsRun` configuration files,
corresponding to different types of PV-related analyses.

An example of how to run a test with one of these cfg files is given below:
```
cd ${CMSSW_BASE}/src/usercode/PrimaryVertexAnalyzer/test/cfg
cmsRun pva_cfg.py maxEvents=10 dumpPython=pva_configDump.py reco=Phase2_D76
```

#### Batch-job workflow at PSI's Tier-3

Submission of multiple jobs to the batch system can be done using
the executables `scripts/bdriver` and `scripts/bmonitor`.

The first one creates the output directory
and the executables to be used by the batch jobs,
while the second one allows to monitor and
manage (e.g. resubmit) the jobs themselves.

For a given set of jobs, one runs the `bdriver` step first (and only once),
and then controls the jobs running `bmonitor` as many times as needed,
until all jobs complete successfully.

**Note**: both scripts support two batch systems:
`HTCondor` (in use on `lxplus` machines)`, and `SLURM` (in use at `T3_PSI_CH`);
the `HTCondor` functionalities are expected to work,
but they are currently under-tested, as most of the development is done at `T3_PSI_CH`.

The commands below show an example of this type of workflow;
in this example, the script `test/prod/bjobs_Phase2_D76vD78_210514.sh`
serves as a wrapper calling `bdriver` for a certain set of DAS samples.
Such a wrapper represents a "production",
i.e. the execution of a certain analysis (i.e. cfg file + cmd-line args)
on a list of input data sets.
Typically, for a new "production" of results the user would write
a new wrapper under `prod/` specifying the relevant input data sets
and configuration file (+ its command-line arguments).
```
# path to output directory on T3 Storage Element (SE)
outdir=/pnfs/psi.ch/cms/trivcat/store/user/${USER}/test/tmp_cmsrun_test1

# wrapper to create scripts for cmsRun jobs to be submitted to the SLURM batch system
${CMSSW_BASE}/src/usercode/PrimaryVertexAnalyzer/test/prod/bjobs_Phase2_D76vD78_210514.sh ${outdir}

# run one job locally
SLURM_ARRAY_TASK_ID=6 ${outdir}/Phase2_D76/RelValTenMuExtendedE0To200_mcRun4_D76_NoPU/slurm_exe.sh

# check status of all the tasks prepared by the driver
bmonitor -i ${outdir}

# submit a max of 100 jobs via SLURM
bmonitor -i ${outdir} -r -m 100
```

#### Additional Notes

(under construction)
