#!/bin/bash

[ _$BATCH == _ ] && BATCH=512
[ _$EPOCH == _ ] && EPOCH=50

OUTDIR=../ZAJJ-CNN/out_results/rescaled_${BATCH}_EPOCH_${EPOCH}

[ -d $OUTDIR ] || mkdir -p $OUTDIR

python train_torch.py -o $OUTDIR --epoch $EPOCH --batch $BATCH -t ../ZAJJ-CNN/input_data/rescaled/preprocessed_train.h5 \
 -v ../ZAJJ-CNN/input_data/rescaled/preprocessed_val.h5

