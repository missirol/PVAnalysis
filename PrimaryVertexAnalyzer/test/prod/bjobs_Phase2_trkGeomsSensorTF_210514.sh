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

samplesMap["RelValTenMuExtendedE0To200_mcRun4_D76_NoPU"]="/RelValTenMuExtendedE_0_200/CMSSW_11_3_0_pre6-113X_mcRun4_realistic_v6_2026D76noPU-v1/GEN-SIM-RECO"
samplesMap["RelValTenMuExtendedE0To200_mcRun4_D78_NoPU"]="/RelValTenMuExtendedE_0_200/CMSSW_11_3_0_pre6-113X_mcRun4_realistic_v6_2026D78noPU-v1/GEN-SIM-RECO"
samplesMap["RelValTenMuExtendedE0To200_mcRun4_D80_NoPU"]="/RelValTenMuExtendedE_0_200/CMSSW_11_3_0_pre6-113X_mcRun4_realistic_v6_2026D80noPU-v1/GEN-SIM-RECO"
samplesMap["RelValTenMuExtendedE0To200_mcRun4_D81_NoPU"]="/RelValTenMuExtendedE_0_200/CMSSW_11_3_0_pre6-113X_mcRun4_realistic_v6_2026D81noPU-v1/GEN-SIM-RECO"

recoKeys=(
  Phase2_D76
  Phase2_D78
  Phase2_D80
  Phase2_D81
)

for recoKey in "${recoKeys[@]}"; do
  python ${CMSSW_BASE}/src/usercode/PrimaryVertexAnalyzer/test/cfg/pva_cfg.py \
    dumpPython=.tmp_${recoKey}_cfg.py numThreads=1 reco=${recoKey}

  for sampleKey in ${!samplesMap[@]}; do

    if [[ ${recoKey} == *D76* ]] && [[ ${sampleKey} != *D76* ]]; then continue; fi;
    if [[ ${recoKey} == *D78* ]] && [[ ${sampleKey} != *D78* ]]; then continue; fi;
    if [[ ${recoKey} == *D80* ]] && [[ ${sampleKey} != *D80* ]]; then continue; fi;
    if [[ ${recoKey} == *D81* ]] && [[ ${sampleKey} != *D81* ]]; then continue; fi;

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
