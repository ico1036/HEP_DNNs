import numpy as np
import pandas as pd
from IPython.display import display

data_df = pd.read_csv('cut_results3.csv',sep=' ')
#display(data_df)


print(data_df.iloc[data_df['Sigma'].idxmax(axis=0)])

'''
Mjj          900.000000
dEta           2.500000
Zepp           2.200000
N_exp_sig     51.118863
N_exp_bkg     69.374917
Sigma          4.660000
'''
