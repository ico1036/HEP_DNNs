import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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


plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)


bins = np.linspace(0,1,100)
plt.hist(hist_pred_sig,bins=bins,color='r',alpha=0.7)
plt.hist(hist_pred_bkg,bins=bins,color='b',alpha=0.7)
plt.xlabel('DNN score')
plt.ylabel('Nuber of events')

#plt.xscale('log')
#plt.yscale('log')

plt.savefig("score.png")

