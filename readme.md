### Setup
```
scram p CMSSW CMSSW_11_2_0_pre3
cd CMSSW_11_2_0_pre3/src
eval `scram runtime -sh`

git cms-addpkg RecoVertex/PrimaryVertexProducer
git clone https://github.com/werdmann/usercode.git usercode -o werdmann -b master

cd /t3home/erdmann/cmssw/CMSSW_11_2_0_pre3/src
git diff > "${CMSSW_BASE}"/src/diff_erdmann.txt

cd usercode
git diff > "${CMSSW_BASE}"/src/usercode/diff_erdmann.txt

cd "${CMSSW_BASE}"/src
git apply diff_erdmann.txt
rm -f diff_erdmann.txt

cd "${CMSSW_BASE}"/src/usercode
git apply diff_erdmann.txt
rm -f diff_erdmann.txt

cd "${CMSSW_BASE}"/src
scram b

cd "${CMSSW_BASE}"/src/usercode

git remote add missirol /work/missiroli_m/test/pv_studies/usercode
git fetch missirol
```
