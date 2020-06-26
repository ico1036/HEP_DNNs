#!/bin/bash

StartTime=$(date +%s)

OUTDIR=$1
TESTDIR=$2

python eval_torch.py -d $OUTDIR  -t $TESTDIR

#python old_eval_torch.py -d $OUTDIR  -t $TESTDIR


EndTime=$(date +%s)
echo "It takes $(($EndTime - $StartTime)) seconds to complete this task."

