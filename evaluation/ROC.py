import numpy as np
import h5py
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix, precision_recall_curve, accuracy_score

path='../data/'

test_data  = np.loadtxt(path+'test_data.csv', delimiter=',')

y_true = test_data[:,-1]
y_true = y_true.astype('int32')

y_pred = np.load('../training/prediction_nn_log.pyc.npy')
print(roc_auc_score(y_true, y_pred))


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


idx_sig = np.where(y_true == 1)[0]
idx_bkg =np.where(y_true == 0)[0]

hist_pred_sig = y_pred[idx_sig]
hist_pred_bkg = y_pred[idx_bkg]


plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)

bins = np.linspace(0,1,100)
plt.hist(hist_pred_sig,bins=bins,color='r',alpha=0.7)
plt.hist(hist_pred_bkg,bins=bins,color='b',alpha=0.7)
plt.savefig("score.png")

