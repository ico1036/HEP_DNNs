import numpy as np
import pandas as pd
from IPython.display import display

data_df = pd.read_csv('train_data.csv',sep=',')
#display(data_df)


## Set cut domain
Domain_Mjj  = [600,700,800,900,1000]
Domain_dEta = list([round(i*0.1,1) for i in range(20,60)])
Domain_zepp = list([round(i*0.1,1) for i in range(10,30)])
Domain_zepp.insert(0,0)



## Cut and count optimizer
for i in range(len(Domain_Mjj)):

	for j in range(len(Domain_dEta)):

		for k in range(len(Domain_zepp)):
			print(Domain_Mjj[i],Domain_dEta[j],Domain_zepp[k],data_df.query('mJJ > @Domain_Mjj[@i] and dEtaJJ > @Domain_dEta[@j] and zepp < @Domain_zepp[@k] and issig > 0')['mJJ'].shape[0],
			data_df.query('mJJ > @Domain_Mjj[@i] and dEtaJJ > @Domain_dEta[@j] and zepp < @Domain_zepp[@k] and issig == 0')['mJJ'].shape[0])


## Draw hist

'''
## Draw hist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)

fig,axs = plt.subplots(1,3,figsize=(60,15))

bins = np.linspace(0,6000,100)
axs[0].hist(data_df.query('issig > 0')['mJJ'],bins=bins,color='r',alpha=0.7,density=True,label='signal')
axs[0].hist(data_df.query('issig == 0')['mJJ'],bins=bins,color='b',alpha=0.7,density=True,label='background')
axs[0].set_title('Mjj',fontsize=40)
axs[0].set_ylabel('N events',fontsize=35)
axs[0].set_xlabel('Mjj',fontsize=35)
axs[0].legend(prop={'size':20})
axs[0].grid(which='major', linestyle='-')
axs[0].minorticks_on()
axs[0].set_yscale('log')

bins = np.linspace(0,10,50)
axs[1].hist(data_df.query('issig > 0')['dEtaJJ'].abs(),bins=bins,color='r',alpha=0.7,density=True,label='signal')
axs[1].hist(data_df.query('issig == 0')['dEtaJJ'].abs(),bins=bins,color='b',alpha=0.7,density=True,label='background')
axs[1].set_title('dEtaJJ',fontsize=40)
axs[1].set_ylabel('N events',fontsize=35)
axs[1].set_xlabel('dEtajj',fontsize=35)
axs[1].legend(prop={'size':20})
axs[1].grid(which='major', linestyle='-')
axs[1].minorticks_on()
axs[1].set_yscale('log')

bins = np.linspace(0,10,50)
axs[2].hist(data_df.query('issig > 0')['zepp'],bins=bins,color='r',alpha=0.7,density=True,label='signal')
axs[2].hist(data_df.query('issig == 0')['zepp'],bins=bins,color='b',alpha=0.7,density=True,label='background')
axs[2].set_title('Zeppen feld',fontsize=40)
axs[2].set_ylabel('N events',fontsize=35)
axs[2].set_xlabel('zepp',fontsize=35)
axs[2].legend(prop={'size':20})
axs[2].grid(which='major', linestyle='-')
axs[2].minorticks_on()
axs[2].set_yscale('log')

#major_ticks = np.arange(0, 1024, 200)
#minor_ticks = np.arange(0, 1024, 100)

#plt.show()
plt.savefig('hist.png')

'''
