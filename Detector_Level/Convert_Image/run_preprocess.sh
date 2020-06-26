
python preprocess.py --train_data outimages_merged/large_size/Signal/Signal1/train.h5 --train_out_name outimages_preprocessed/large_size/Signal1/preprocessed_train.h5 --model "3ch-CNN"
python preprocess.py --val_data outimages_merged/large_size/Signal/Signal1/val.h5 --val_out_name outimages_preprocessed/large_size/Signal1/preprocessed_val.h5 --model "3ch-CNN"
python preprocess.py --test_data outimages_merged/large_size/Signal/Signal1/test.h5 --test_out_name outimages_preprocessed/large_size/Signal1/preprocessed_test.h5 --model "3ch-CNN"

python preprocess.py --train_data outimages_merged/large_size/Signal/Signal2/train.h5 --train_out_name outimages_preprocessed/large_size/Signal2/preprocessed_train.h5 --model "3ch-CNN"
python preprocess.py --val_data outimages_merged/large_size/Signal/Signal2/val.h5 --val_out_name outimages_preprocessed/large_size/Signal2/preprocessed_val.h5 --model "3ch-CNN"
python preprocess.py --test_data outimages_merged/large_size/Signal/Signal2/test.h5 --test_out_name outimages_preprocessed/large_size/Signal2/preprocessed_test.h5 --model "3ch-CNN"

python preprocess.py --train_data outimages_merged/large_size/Signal/Signal3/train.h5 --train_out_name outimages_preprocessed/large_size/Signal3/preprocessed_train.h5 --model "3ch-CNN"
python preprocess.py --val_data outimages_merged/large_size/Signal/Signal3/val.h5 --val_out_name outimages_preprocessed/large_size/Signal3/preprocessed_val.h5 --model "3ch-CNN"
python preprocess.py --test_data outimages_merged/large_size/Signal/Signal3/test.h5 --test_out_name outimages_preprocessed/large_size/Signal3/preprocessed_test.h5 --model "3ch-CNN"

python preprocess.py --train_data outimages_merged/large_size/BKG/QCD120/train.h5 --train_out_name outimages_preprocessed/large_size/QCD120/preprocessed_train.h5 --model "3ch-CNN"
python preprocess.py --val_data outimages_merged/large_size/BKG/QCD120/val.h5 --val_out_name outimages_preprocessed/large_size/QCD120/preprocessed_val.h5 --model "3ch-CNN"
python preprocess.py --test_data outimages_merged/large_size/BKG/QCD120/test.h5 --test_out_name outimages_preprocessed/large_size/QCD120/preprocessed_test.h5 --model "3ch-CNN"

python preprocess.py --train_data outimages_merged/large_size/BKG/QCD600/train.h5 --train_out_name outimages_preprocessed/large_size/QCD600/preprocessed_train.h5 --model "3ch-CNN"
python preprocess.py --val_data outimages_merged/large_size/BKG/QCD600/val.h5 --val_out_name outimages_preprocessed/large_size/QCD600/preprocessed_val.h5 --model "3ch-CNN"
python preprocess.py --test_data outimages_merged/large_size/BKG/QCD600/test.h5 --test_out_name outimages_preprocessed/large_size/QCD600/preprocessed_test.h5 --model "3ch-CNN"

python preprocess.py --train_data outimages_merged/large_size/BKG/QCD1000/train.h5 --train_out_name outimages_preprocessed/large_size/QCD1000/preprocessed_train.h5 --model "3ch-CNN"
python preprocess.py --val_data outimages_merged/large_size/BKG/QCD1000/val.h5 --val_out_name outimages_preprocessed/large_size/QCD1000/preprocessed_val.h5 --model "3ch-CNN"
python preprocess.py --test_data outimages_merged/large_size/BKG/QCD1000/test.h5 --test_out_name outimages_preprocessed/large_size/QCD1000/preprocessed_test.h5 --model "3ch-CNN"







