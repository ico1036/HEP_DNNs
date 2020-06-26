#!/bin/bash


export SCRAM_ARCH=slc6_amd64_gcc630
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
echo "$VO_CMS_SW_DIR $SCRAM_ARCH"
source ${VO_CMS_SW_DIR}/cmsset_default.sh
cd /x5/cms/jwkim/Delphes_NEW/CMSSW_9_1_0_pre3/src
eval `scramv1 runtime -sh`
cd -

## -- header file
export PATH=/x5/cms/jwkim/Delphes_NEW/Delphes3.4.2/classes:$PATH

## -- lib file
export LD_LIBRARY_PATH=/x5/cms/jwkim/Delphes_NEW/Delphes3.4.2:$LD_LIBRARY_PATH




thisIndex=$1
maxFile=$2
listFile=$3
type_=$4
xsec=$5



firstIndex=`expr $thisIndex \* $maxFile + 1`
lastIndex=`expr $firstIndex + $maxFile - 1`
inFiles=""
index=0

for file in `cat $listFile`
do
    ((index++))
    if [ $index -ge $firstIndex ] && [ $index -le $lastIndex ]; then
        echo "$index $file"
        inFiles="$inFiles $file"
    fi
done


outfilename="preproc__QCDZAJJ_${thisIndex}.root"

/x5/cms/jwkim/MG5_aMC_v2_6_4/MLzajj_Learn/Ntuple/preprocess.exe $outfilename $type_ $xsec $inFiles


#df -h


#echo "outfile: " $outfilename
#echo $inFiles
