import numpy as np
import pandas as pd
from IPython.display import display

data_df = pd.read_csv('cut_results.csv',sep=' ')
#display(data_df)


print(data_df.iloc[data_df['Sigma'].idxmax(axis=0)])
'''
Mjj          900.000000
dEta           2.500000
Zepp           2.100000
N_exp_sig     51.090706
N_exp_bkg     69.340594
Sigma          4.660000

'''


