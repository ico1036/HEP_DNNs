import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Path
dir_   ='train_log.csv'

# csv to dataframe
df   = pd.read_csv(dir_)

fig,axs = plt.subplots(2,1,figsize=(20,20))
plt.rc('xtick',labelsize=30)
plt.rc('ytick',labelsize=30)
x_loss = np.arange(len(df['loss']))
x_acc = np.arange(len(df['acc']))

# --Epoch vs loss

axs[0].plot(x_loss + 1,df['loss'],'--bo',color='darkorange',linewidth=4,markersize=10,label='Train-set')
axs[0].plot(x_loss + 1,df['val_loss'],'--bo',color='royalblue',linewidth=4,markersize=10,label='Validation-set')

#axs[0].set_yscale('log')
axs[0].set_title('epoch vs loss',fontsize=50)
axs[0].set_xlabel('epoch',fontsize=45)
axs[0].set_ylabel('loss',fontsize=45)
axs[0].legend(prop={'size':40})
axs[0].grid(which='major', linestyle='-')
axs[0].minorticks_on()

# --Epoch vs acc

axs[1].plot(x_acc + 1,df['acc'],'--bo',color='darkorange',linewidth=4,markersize=10,label='Train-set')
axs[1].plot(x_acc + 1,df['val_acc'],'--bo',color='royalblue',linewidth=4,markersize=10,label='Validation-set')

#axs[1].set_yscale('log')
axs[1].set_title('epoch vs acc',fontsize=50)
axs[1].set_xlabel('epoch',fontsize=45)
axs[1].set_ylabel('loss',fontsize=45)
axs[1].legend(prop={'size':40})
axs[1].grid(which='major', linestyle='-')
axs[1].minorticks_on()

fig.tight_layout()
plt.savefig('monitoring.png')
