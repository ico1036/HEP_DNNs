import numpy as np
import pandas as pd

data_df = pd.read_csv('optimized_results_60Z120.csv',sep=',')


print(data_df.iloc[data_df['Sigma'].idxmax(axis=0)])



'''
60 < Zmass < 120
Mjj          1100.000000
dEta            2.500000
Zepp            1.700000
N_exp_sig      58.867806
N_exp_bkg      64.682506
Sigma           5.300000
'''


'''
70 < Zmass < 110
Mjj          1100.000000
dEta            2.800000
Zepp            1.700000
N_exp_sig      55.854541
N_exp_bkg      52.922674
Sigma           5.360000
'''
