#!/bin/bash


## Try Large Size Image


files_Signal=`ls -1 ../condor_out_Signal_list/*.root`
files_QCD120=`ls -1 ../condor_out_QCD120_list/*.root`
files_QCD600=`ls -1 ../condor_out_QCD600_list/*.root`
files_QCD1000=`ls -1 ../condor_out_QCD1000_list/*.root`




#python prepare_data_my.py --input-type delphes --output-h5 Signal_sample_out.h5 --bins 224 --GenEvt 1499322 ../condor_out_Signal_list/preproc__QCDZAJJ_44.root



#cnt=0
#for f in $files_Signal:
#do
#cnt=`expr $cnt + 1`
#outname="Signalimage_${cnt}.h5"
#echo $f $outname
#python prepare_data_my.py --input-type delphes --output-h5 outimages/large_size/$outname --bins 224 --GenEvt 1499322 $f
#done
#
#echo " "


cnt=0
for f in $files_QCD120:
do
cnt=`expr $cnt + 1`
outname="QCD120image_${cnt}.h5"
echo $f $outname
python prepare_data_my.py --input-type delphes --output-h5 outimages/large_size/$outname --bins 224 --GenEvt 999986 $f
done

echo " "

'''
cnt=0
for f in $files_QCD600:
do
cnt=`expr $cnt + 1`
outname="QCD600image_${cnt}.h5"
echo $f $outname
python prepare_data_my.py --input-type delphes --output-h5 outimages/large_size/$outname --bins 224 --GenEvt 999986 $f
done

echo " "



cnt=0
for f in $files_QCD1000:
do
cnt=`expr $cnt + 1`
outname="QCD1000image_${cnt}.h5"
echo $f $outname
python prepare_data_my.py --input-type delphes --output-h5 outimages/large_size/$outname --bins 224 --GenEvt 999835 $f
done

'''

