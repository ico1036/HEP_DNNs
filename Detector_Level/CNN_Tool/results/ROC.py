import pandas as pd
from sklearn.metrics import roc_curve, roc_auc_score
import numpy as np
import h5py


# -- Read file


f = h5py.File('input_data/preprocessed_test.h5')
pred_dir  = 'out_results/rescaled_512_EPOCH_50' 

w = f['all_events']['weights_val'][:]
y_true = f['all_events']['labels_val'][:]



predFile = pred_dir + '/prediction_norescal_to_test.csv'
df = pd.read_csv(predFile)
tpr, fpr, thr = roc_curve(df['label'], df['prediction'], pos_label=0)
auc = roc_auc_score(df['label'], df['prediction'])

print("##### --auc: ",auc)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Cut based  TPR FPR
x_dot = 0.054 
y_dot = 0.259 
cut_based_acc = 0.606


plt.plot(x_dot, y_dot, 'o', label='Cut-based selection')
plt.plot(fpr, tpr,'-', color='darkred',label='AUC: %f' %(auc))
plt.legend(['physics selection]'],prop={'size' :20})
plt.vlines(x_dot, ymin=0, ymax=1, linestyle='dashed', alpha=0.5, color='black')
plt.xlabel('1 - Background rejection')
plt.ylabel('Signal efficiency')
plt.xlim(-0.01, 1)
plt.ylim(0, 1.01)
plt.legend()
plt.grid(which='major', linestyle='--')
plt.minorticks_on()
plt.savefig(pred_dir + '/ROC.png')
