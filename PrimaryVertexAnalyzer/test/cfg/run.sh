#!/bin/bash

set -e

declare -A minPtMap
minPtMap["minPt0p0"]=0.0
minPtMap["minPt0p3"]=0.3
minPtMap["minPt0p5"]=0.5
minPtMap["minPt0p7"]=0.7
minPtMap["minPt1p0"]=1.0

inputFiles=(
 "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/B994C571-BDCB-2F4C-A6EA-87AD7EF439F9.root"
 "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/414714DB-67FA-4A4A-8F9C-C97C2157982C.root"
 "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/EC754AE7-6DAA-7B43-B65E-BE3686E8491E.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/FE624146-477A-B842-9785-2DA6EA6F915B.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/AEE888E2-7CE7-164E-BF06-B2538AA17540.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/AB8642F6-4A7E-4447-98B5-1FF81E15C14C.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/DB3868C5-9D59-A04B-BD24-B580ED878E64.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/20A32BF0-7DFB-0D42-8FF6-547951404FE5.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/AC79CD5A-6D68-F943-A213-E758DDA44935.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/E1A8E99A-7C2C-9A47-8989-DB93B56AD9C7.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/144B54C3-0E70-FD47-B7C4-4BCD1BDEC8FF.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/A28A28A7-38F1-4C44-9474-DE8DA08479B4.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/5E0EB771-3A27-4F41-ADC0-B5B8906F0C27.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/3265900D-915A-1743-A292-02F168BFD2F6.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/B7A52626-4828-3B4D-BDC6-5FC79740748C.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/566385A8-46D0-BF42-8D19-1BEE241B7D0E.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/4EE15837-9B12-D649-927A-30234E4A1921.root"
# "/store/relval/CMSSW_11_2_0_pre3/RelValZMM_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v5-v1/20000/B67FC924-59C4-A44F-AFE5-9B5E45A8B2F2.root"
)
inputFilesStr=$( IFS=$','; echo "${inputFiles[*]}" )

for minPtKey in ${!minPtMap[@]}; do
  minPtVal=${minPtMap[${minPtKey}]}
  cmsRun pv3_cfg.py input=${inputFilesStr} events=-1 info=Run3_ZMM_${minPtKey} redoPV=True 4D=False era=Run3 minPt=${minPtVal} outputFile=pv_Run3_ZMM_${minPtKey}.root
  unset minPtVal
done
unset minPtKey
unset minPtMap inputFiles inputFilesStr
