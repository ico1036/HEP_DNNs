## 32PU CNT
#source run_eval.sh CMS_Baeline_with1000_selected_balanced/32PU_TrackCnt_512_EPOCH_50 ../../../NERSC_work/HEPdata_NEW/Merging_dir_forHT700bin/2020_CMScut_32PU_v2_full/Distributed/preproc_cnt/Preprocessed_test.h5

## 32PU PT
#source run_eval.sh CMS_Baeline_Full/32PU_TrackPT_512_EPOCH_50/  ../../../NERSC_work/HEPdata_NEW/Merging_dir_forHT700bin/2020_CMScut_32PU_v2_full/Preprocessed_TrackPT/Preprocessed_test.h5


## ----Validatae "Without 1000 model" using with 1000 model

# Track Cnt
#source run_eval.sh CMS_Baseline_v1/CMS_Baeline_32PU_TrackCnt_512_EPOCH_50/ ../../Data_directory/32PU_fulldata/preprocessed_cnt/PreprocNrescaled_test_HT1000nRPV.h5


# Track PT
#source run_eval.sh CMS_Baseline_v1/CMS_Baeline_32PU_TrackPT_512_EPOCH_50/ ../../Data_directory/32PU_fulldata/preprocessed_pt/PreprocNrescaled_test_HT1000nRPV.h5


#### ZAJJ ---

source run_eval.sh ../ZAJJ-CNN/out_results/rescaled_512_EPOCH_50/ ../ZAJJ-CNN/input_data/preprocessed_test.h5


#### 2019 ---

#source run_eval.sh ../../../RPVSUSY2020paper/AfterPM/KMPBLOCKTIME_1__SELECT_64__MPIPROC_64__THREADS_64__BATCH_512/ ../data/2019_data/Preprocessed_Test.h5
