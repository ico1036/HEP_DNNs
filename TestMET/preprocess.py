import pandas as pd
from ROOT import *
from root_numpy import root2array, tree2array
from root_numpy import testdata
from IPython.display import display
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if __name__ == '__main__':

	# --Ntuple to Numpy
	_file 	  = TFile.Open('data/ntDelphes_pp2w2enu.root')
	_tree 	  = _file.Get('tree')
	data_arr  = tree2array(_tree)
	data_all_df   = pd.DataFrame(data_arr)
	
	data_df = data_all_df[['l1Pt','l1Eta','l1Phi','l1E','l2Pt','l2Eta','l2Phi','l2E']]

	
	# --Statistics
	train_stats = data_df.describe()
	train_stats.pop('l2Eta')
	train_stats = train_stats.transpose()
	display(train_stats)


	#data_df.hist(bins=50, figsize=(20,15))
	#plt.savefig('hist.png')
	
	
	data = data_df.values
	
	
	
	# --Shuffle and Split dataset: Trainig, Validation, Test
	inds = np.arange(data.shape[0])
	tr   = int(0.8 * data.shape[0])  # Split ratio --> 6 : 2: 2
	np.random.RandomState(11).shuffle(inds)
	
	train_data = data[inds[:tr]]
	rest_data   = data[inds[tr:]]
	val_data = rest_data[:int(rest_data.shape[0] /2)]
	test_data = rest_data[int(rest_data.shape[0] /2):]
	
	print(train_data.shape)
	print(val_data.shape)
	print(test_data.shape)
	
	# --Write data as csv format
	#np.savetxt('data/train_data.csv',train_data,fmt='%5.5f',header='l1Pt,l1Eta,l1Phi,l1E,l2Pt,l2Eta,l2Phi,l2E',delimiter=',')
	#np.savetxt('data/val_data.csv',val_data,fmt='%5.5f',header='l1Pt,l1Eta,l1Phi,l1E,l2Pt,l2Eta,l2Phi,l2E',delimiter =',')
	#np.savetxt('data/test_data.csv',test_data,fmt='%5.5f',header='l1Pt,l1Eta,l1Phi,l1E,l2Pt,l2Eta,l2Phi,l2E',delimiter =',')


   
