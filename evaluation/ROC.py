import numpy as np
import h5py
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix, precision_recall_curve, accuracy_score
import pandas as pd


path='../data/data_normal_by_all/'

test_data  =pd.read_csv(path+'test_data.csv', sep=',')

y_true = test_data['issig']

y_true = y_true.astype('int32')

y_pred = np.load('../training/prediction_nn_log.pyc.npy')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


## --AUC out
tpr, fpr, thr = roc_curve(y_true, y_pred, pos_label=0)
auc = roc_auc_score(y_true, y_pred)
print("AUC: ", auc)

x_dot = 0.082
y_dot = 0.288


plt.plot(fpr, tpr,color='midnightblue',label='ROC')
plt.plot(x_dot, y_dot, 'o', label='Cut based selection')
plt.vlines(x_dot, ymin=0, ymax=1, linestyle='dashed', alpha=0.5, color='black')
plt.xlabel('False postive rate')
plt.ylabel('True positive rate')
plt.xlim(-0.01,1.)
plt.ylim(0,1.01)
plt.legend()
plt.grid(which='major', linestyle='--')
plt.minorticks_on()
plt.savefig("ROC.png")


