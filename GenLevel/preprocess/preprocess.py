import pandas as pd
from ROOT import *
from root_numpy import root2array, tree2array
from root_numpy import testdata
from IPython.display import display
import numpy as np


path='../data/'

# --read signal dataset
sig_file = TFile.Open(path+'sig.root') 
sig_tree = sig_file.Get('ntuple')   
sig_arr  = tree2array(sig_tree)	
sig_df   = pd.DataFrame(sig_arr)	

# --read background dataset
bkg_file = TFile.Open(path+'bkg.root') 
bkg_tree = bkg_file.Get('ntuple')   
bkg_arr  = tree2array(bkg_tree)	
bkg_df   = pd.DataFrame(bkg_arr)	

print('sig: ', sig_df.shape[0])
print('bkg: ', bkg_df.shape[0])


# --Normalize
def MinMaxScaler(data):
	numerator = data - np.min(data,0)
	denominator = np.max(data,0) - np.min(data,0)
	denominator = denominator.astype('float')
	return numerator / denominator
    #return numerator / (denominator+1e-7)

norm=True
if norm == True :
	sig_df = MinMaxScaler(sig_df)
	bkg_df = MinMaxScaler(bkg_df)

# --Add Label
sig_df['issig'] = 1
bkg_df['issig'] = 0


# --Merge signal and bkg dataset
data_df = pd.concat([sig_df,bkg_df],ignore_index=True)


display(data_df)
data = data_df.values


# --Shuffle and Split dataset: Trainig, Validation, Test
inds = np.arange(data.shape[0])
tr   = int(0.6 * data.shape[0])  # Split ratio --> 6 : 2: 2
np.random.RandomState(11).shuffle(inds)

train_data = data[inds[:tr]]
rest_data   = data[inds[tr:]]
val_data = rest_data[:int(rest_data.shape[0] /2)]
test_data = rest_data[int(rest_data.shape[0] /2):]

print(train_data.shape)
print(val_data.shape)
print(test_data.shape)


# --Write data as csv format
#np.savetxt(path+'train_data.csv',train_data,fmt='%5.5f',delimiter =',')
#np.savetxt(path+'val_data.csv',val_data,fmt='%5.5f',delimiter =',')
#np.savetxt(path+'test_data.csv',test_data,fmt='%5.5f',delimiter =',')




