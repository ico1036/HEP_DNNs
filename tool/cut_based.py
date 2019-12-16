import numpy as np
import pandas as pd
from IPython.display import display
import math

data_df = pd.read_csv('../data/un_normalized/all_data.csv',sep=',')
#display(data_df)

## cross-section
xsec_sig = 0.004942
xsec_bkg = 0.02353
N_gen_sig = data_df.query('issig > 0').shape[0]
N_gen_bkg = data_df.query('issig == 0').shape[0]

Lumi=35900
#Lumi=150000

data_df['dEtaJJ'] = data_df['dEtaJJ'].abs()
data_df['zepp']   = data_df['zepp'].abs()


print(data_df.describe())
print("xsec sig: ",xsec_sig)
print("xsec bkg: ",xsec_bkg)
print("Signal Gen events: ",N_gen_sig)
print("BKG    Gen events: ",N_gen_bkg)
print("Start optimize ... ")


## Cut results -----------------------------------

'''
Mjj          800.000000
dEta           2.400000
Zepp           1.600000
N_exp_sig    106.249527
N_exp_bkg    114.147731
Sigma          7.160000
'''

Mjjcut  = 800
dEtacut = 2.4
Zeppcut =  1.6

# Confusion matrix
TP = data_df.query('mJJ > @Mjjcut  and dEtaJJ > @dEtacut  and zepp < @Zeppcut  and issig > 0')['mJJ'].shape[0]
FN = N_gen_sig - TP
FP = data_df.query('mJJ > @Mjjcut  and dEtaJJ > @dEtacut  and zepp < @Zeppcut  and issig == 0')['mJJ'].shape[0]
TN = N_gen_bkg - FP

TPR = TP / float(N_gen_sig)
FPR = FP / float(N_gen_bkg)
ACC = (TP+TN) / float(N_gen_sig+N_gen_bkg)


print("Xsec sig: ",xsec_sig)
print("Xsec bkg: ",xsec_bkg)
print("Gen sig: ",N_gen_sig)
print("Gen bkg: ",N_gen_bkg)
print("TPR: ",round(TPR,3))
print("FPR: ",round(FPR,3))
print("ACC: ",round(ACC,3))


'''
## ----------------- Cut scanner


## Set cut domain
Domain_Mjj  = [500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500]
Domain_dEta = list([round(i*0.1,1) for i in range(0,60)])
Domain_zepp = list([round(i*0.1,1) for i in range(0,50)])
Domain_zepp.reverse()

print("Mjj  dEta Zepp N_exp_sig N_exp_bkg Sigma")
for i in range(len(Domain_Mjj)):

	for j in range(len(Domain_dEta)):

		for k in range(len(Domain_zepp)):
			

			N_sig = data_df.query('mJJ > @Domain_Mjj[@i] and dEtaJJ > @Domain_dEta[@j] and zepp < @Domain_zepp[@k] and issig > 0')['mJJ'].shape[0]
			N_bkg = data_df.query('mJJ > @Domain_Mjj[@i] and dEtaJJ > @Domain_dEta[@j] and zepp < @Domain_zepp[@k] and issig == 0')['mJJ'].shape[0]

			N_exp_sig = N_sig * xsec_sig *Lumi / N_gen_sig
			N_exp_bkg = N_bkg * xsec_bkg *Lumi / N_gen_bkg
			
			if(N_exp_sig+N_exp_bkg ==0):
				continue;
			Sigma = N_exp_sig / math.sqrt( N_exp_sig+N_exp_bkg )
			print Domain_Mjj[i],Domain_dEta[j],Domain_zepp[k],N_exp_sig,N_exp_bkg,round(Sigma,2)

## -----------------------------------------------	
'''


'''
## -------------Draw hist

weight_sig  = np.ones(data_df.query('issig > 0')['mJJ'].shape) * xsec_sig * Lumi / N_gen_sig
weight_bkg  = np.ones(data_df.query('issig ==0')['mJJ'].shape) * xsec_bkg * Lumi / N_gen_bkg

print(weight_sig.shape)
print(weight_bkg.shape)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rc('xtick',labelsize=50)
plt.rc('ytick',labelsize=50)

fig,axs = plt.subplots(1,3,figsize=(90,25))

bins = np.linspace(0,6000,100)
axs[0].hist(data_df.query('issig > 0')['mJJ'],bins=bins,color='r',alpha=0.7,weights=weight_sig, histtype='step',linewidth=6,label='signal')
axs[0].hist(data_df.query('issig == 0')['mJJ'],bins=bins,color='b',alpha=0.7,weights=weight_bkg, histtype='step',linewidth=6,label='background')
axs[0].set_ylabel('N events',fontsize=70)
axs[0].set_xlabel('$M_{JJ}$',fontsize=70)
axs[0].legend(prop={'size':50})
axs[0].grid(which='major', linestyle='-')
axs[0].minorticks_on()
axs[0].set_yscale('log')

bins = np.linspace(0,10,50)
axs[1].hist(data_df.query('issig > 0')['dEtaJJ'].abs(),bins=bins,color='r',alpha=0.7,weights=weight_sig,histtype='step',linewidth=6,label='signal')
axs[1].hist(data_df.query('issig == 0')['dEtaJJ'].abs(),bins=bins,color='b',alpha=0.7,weights=weight_bkg,histtype='step',linewidth=6,label='background')
axs[1].set_ylabel('N events',fontsize=70)
axs[1].set_xlabel('$\Delta\eta_{jj}$',fontsize=70)
axs[1].legend(prop={'size':50})
axs[1].grid(which='major', linestyle='-')
axs[1].minorticks_on()
axs[1].set_yscale('log')

bins = np.linspace(0,10,50)
axs[2].hist(data_df.query('issig > 0')['zepp'],bins=bins,color='r',alpha=0.7,weights=weight_sig,histtype='step',linewidth=6,label='signal')
axs[2].hist(data_df.query('issig == 0')['zepp'],bins=bins,color='b',alpha=0.7,weights=weight_bkg,histtype='step',linewidth=6,label='background')
axs[2].set_ylabel('N events',fontsize=70)
axs[2].set_xlabel('Zeppenfeld variable',fontsize=70)
axs[2].legend(prop={'size':50})
axs[2].grid(which='major', linestyle='-')
axs[2].minorticks_on()
axs[2].set_yscale('log')

plt.tight_layout()
#major_ticks = np.arange(0, 1024, 200)
#minor_ticks = np.arange(0, 1024, 100)

#plt.show()
plt.savefig('hist.png')

## ---------------------------------------------------
'''
