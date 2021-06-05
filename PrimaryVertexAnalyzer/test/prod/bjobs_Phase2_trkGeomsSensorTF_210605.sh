#!/bin/bash -e

if [ $# -lt 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=-1
ODIR=${1}

if [ -d ${ODIR} ]; then
  printf "%s\n" "output directory already exists: ${ODIR}"
  exit 1
fi

declare -A samplesMap

samplesMap["RelValTTbar_14TeV_mcRun4_D64_PU200"]="/RelValTTbar_14TeV/CMSSW_11_3_0_pre3-PU_113X_mcRun4_realistic_v3_2026D64PU-v2/GEN-SIM-RECO"
samplesMap["RelValTTbar_14TeV_mcRun4_D66_PU200"]="/RelValTTbar_14TeV/CMSSW_11_3_0_pre3-PU_113X_mcRun4_realistic_v3_2026D66PU-v2/GEN-SIM-RECO"

recoKeys=(
  Phase2_D64
  Phase2_D66
)

for recoKey in "${recoKeys[@]}"; do
  python ${CMSSW_BASE}/src/usercode/PrimaryVertexAnalyzer/test/cfg/pva_cfg.py \
    dumpPython=.tmp_${recoKey}_cfg.py numThreads=1 reco=${recoKey}

  for sampleKey in ${!samplesMap[@]}; do

    if [[ ${recoKey} == *D64* ]] && [[ ${sampleKey} != *D64* ]]; then continue; fi;
    if [[ ${recoKey} == *D66* ]] && [[ ${sampleKey} != *D66* ]]; then continue; fi;

    sampleName=${samplesMap[${sampleKey}]}

    # number of events per sample
    numEvents=${NEVT}
#    if [[ ${sampleKey} == *MinBias* ]]; then
#      numEvents=2000000
#    fi

    bdriver -c .tmp_${recoKey}_cfg.py --customize-cfg -m ${numEvents} \
      -n 500 --cpus 1 --mem 1G --time 00:20:00 \
      -d ${sampleName} -p 0 -o ${ODIR}/${recoKey}/${sampleKey}

    rm -f .tmp_${recoKey}_cfg.py
  done
  unset sampleKey numEvents sampleName

done
unset recoKey recoKeys samplesMap NEVT ODIR
