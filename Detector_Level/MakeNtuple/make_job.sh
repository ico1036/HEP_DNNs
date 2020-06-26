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


#Signal_xsec=0.01291
#QCD120_xsec=0.5274
#QCD600_xsec=0.02727
#QCD1000_xsec=0.008706

##-- Parameters
#################################
filelist=Signal_list
outdir=condor_out_Signal_list
type_=1
xsec=0.01291
##################################

maxfile=30
tmp=/x5/cms/jwkim/MG5_aMC_v2_6_4/MLzajj_Learn/Ntuple/$outdir
if [ ! -d $tmp ]; then mkdir $tmp; fi
cp batch_run.sh $tmp
cp $filelist $tmp

nfile=`cat $filelist | wc -l`
nfile=`expr $maxfile + $nfile - 1`
nJob=`expr $nfile / $maxfile`

cat << EOF > $tmp/job.jds
executable = batch_run.sh
universe = vanilla
output   = condorOut_\$(Process).out
error    = condorErr_\$(Process).err
log      = condor_logfile.log
should_transfer_files = yes
transfer_input_files = $filelist
when_to_transfer_output = ON_EXIT
requirements = (machine != "wn3015.sdfarm.kr")
requirements = \$(requirements) && (machine != "wn3021.sdfarm.kr")
requirements = \$(requirements) && (machine != "wn3012.sdfarm.kr")
arguments = \$(Process) $maxfile $filelist $type_ $xsec
queue $nJob
EOF



cd $tmp
condor_submit job.jds
