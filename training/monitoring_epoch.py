import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Path
dir_   ='train_log.csv'

# csv to dataframe
df   = pd.read_csv(dir_)


plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)

## ---Select Loss or Acc
#target ='loss'
target ='acc'

x = np.arange(len(df['loss']))

train_label_name = "Train-set "+target
val_label_name   = "Validation-set "+target
title ="epoch vs "+target
val_title='epoch vs val_'+target
filename=target+'.png'

fig,axs = plt.subplots(2,1,figsize=(20,20))
axs[0].plot(x+1,df[target],'--bo',color='darkred',label=train_label_name)


axs[0].get_xaxis().get_major_formatter().set_useOffset(False)
axs[0].get_yaxis().get_major_formatter().set_useOffset(False)
#axs[0].set_yscale('log')
axs[0].set_title(title,fontsize=50)
axs[0].set_xlabel('epoch',fontsize=45)
axs[0].set_ylabel(target,fontsize=45)
axs[0].grid()

axs[1].get_xaxis().get_major_formatter().set_useOffset(False)
axs[1].get_yaxis().get_major_formatter().set_useOffset(False)
axs[1].plot(x+1,df['val_'+target],'--bo',color='darkred',label=val_label_name)
#axs[1].set_yscale('log')
axs[1].set_title(val_title,fontsize=50)
axs[1].set_xlabel('epoch',fontsize=45)
axs[1].set_ylabel(target,fontsize=45)

axs[1].grid()

fig.tight_layout()
plt.savefig(filename)

