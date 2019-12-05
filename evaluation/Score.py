import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

Xsec_sig = 0.004942
Xsec_bkg = 0.02353
Gen_sig  = 443712
Gen_bkg  = 444288
Lumi	 = 35900

path='../data/data_normal_by_all/'

test_data  =pd.read_csv(path+'test_data.csv', sep=',')

y_true = test_data['issig']

y_true = y_true.astype('int32')

y_pred = np.load('../training/prediction_nn_log.pyc.npy')



## --Score out
idx_sig = np.where(y_true == 1)[0]
idx_bkg =np.where(y_true == 0)[0]

hist_pred_sig = y_pred[idx_sig]
hist_pred_bkg = y_pred[idx_bkg]


weight_sig = np.ones(hist_pred_sig.shape) * Xsec_sig / Gen_sig * Lumi
weight_bkg = np.ones(hist_pred_bkg.shape) * Xsec_bkg / Gen_bkg * Lumi



plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)
plt.rcParams["figure.figsize"] = (8,8)


bins = np.linspace(0,1,100)
normed_hist_sig = plt.hist(hist_pred_sig,bins=bins,color='r',histtype='step',linewidth=3,weights=weight_sig,label='DNN signal')
normed_hist_bkg = plt.hist(hist_pred_bkg,bins=bins,color='b',histtype='step',linewidth=3,weights=weight_bkg,label='DNN background')
plt.xlabel('DNN score',fontsize=25)
plt.ylabel('Nuber of events',fontsize=25)
plt.legend(prop={'size':15})

#plt.xscale('log')
#plt.yscale('log')

plt.grid(which='major', linestyle='-')
plt.minorticks_on()

plt.tight_layout()

print(hist_pred_sig)
print(normed_hist_sig)


plt.savefig("normed_score.png")

