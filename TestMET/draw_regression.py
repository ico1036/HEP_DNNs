import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from IPython.display import display


y_pred = np.load('prediction_nn_log.pyc.npy')

test_df = pd.read_csv('data/test_data.csv',sep=',')
y_test  = test_df['l2Eta']

plt.rcParams["figure.figsize"] = (40,40)
plt.rc('xtick',labelsize=40)
plt.rc('ytick',labelsize=40)

bins=50
plt.hist(y_test,bins=bins,color='r',histtype='step',linewidth=10,label='real')
plt.hist(y_pred,bins=bins,color='b',histtype='step',linewidth=10,label='prediction')
plt.legend(prop={'size':40})
plt.grid(which='major', linestyle='-')
plt.minorticks_on()
plt.savefig('results.png')
