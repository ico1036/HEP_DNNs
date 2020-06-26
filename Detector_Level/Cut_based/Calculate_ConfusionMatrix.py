from ROOT import *
from root_numpy import root2array, tree2array
import glob
import pandas as pd
import math


def get_tree(files,treename, branch_dict):

	try:
		tree = root2array(files,treename=treename,branches=branch_dict.keys())

	except IOError as e:
		print('WARNING: root2array gave an IOError:', e)
		return None


	tree.dtype.names = branch_dict.values()
	return tree


branch_dict={

'nteeM'	 : 'eeM',
'ntjjM'	 : 'Mjj',
'ntjdEta'   : 'dEtajj',
'ntjdPhi'   : 'dPhijj',
'ntZpVar'   : 'Zepp',
'nttype'	: 'y',
'ntxsec'	: 'xsec',
'ntgenN'	: 'Ngen'

}

Lumi = 150000

infile_name_signal  = glob.glob("../condor_out_Signal_list/preproc__QCDZAJJ_*.root")
infile_name_QCD120  = glob.glob("../condor_out_QCD120_list/preproc__QCDZAJJ_*.root")
infile_name_QCD600  = glob.glob("../condor_out_QCD600_list/preproc__QCDZAJJ_*.root")
infile_name_QCD1000 = glob.glob("../condor_out_QCD1000_list/preproc__QCDZAJJ_*.root")


#infile_name = infile_name_signal + infile_name_QCD120 + infile_name_QCD600 + infile_name_QCD1000

tree_sig = get_tree(infile_name_signal,'tree',branch_dict)
sig_df = pd.DataFrame(tree_sig)

tree_QCD120 = get_tree(infile_name_QCD120,'tree',branch_dict)
QCD120_df = pd.DataFrame(tree_QCD120)

tree_QCD600 = get_tree(infile_name_QCD600,'tree',branch_dict)
QCD600_df = pd.DataFrame(tree_QCD600)

tree_QCD1000 = get_tree(infile_name_QCD1000,'tree',branch_dict)
QCD1000_df = pd.DataFrame(tree_QCD1000)



# --Z mass window
sig_df	   = sig_df.drop(sig_df[(sig_df['eeM'] < 70) | (sig_df['eeM'] > 110)].index)
QCD120_df  = QCD120_df.drop(QCD120_df[(QCD120_df['eeM'] < 70) | (QCD120_df['eeM'] > 110)].index)
QCD600_df  = QCD600_df.drop(QCD600_df[(QCD600_df['eeM'] < 70) | (QCD600_df['eeM'] > 110)].index)
QCD1000_df = QCD1000_df.drop(QCD1000_df[(QCD1000_df['eeM'] < 70) | (QCD1000_df['eeM'] > 110)].index)


xsec_sig = 0.01291
xsec_QCD120 = 0.5274
xsec_QCD600 = 0.02727
xsec_QCD1000 = 0.008706


gen_sig = 1499322.
gen_QCD120 = 999986.
gen_QCD600 = 999986.
gen_QCD1000 = 999835.


sel_sig = 170194
sel_QCD120 = 56625
sel_QCD600 = 56625
sel_QCD1000 = 60368


'''
70 < Z < 110
Mjj          1100.000000
dEta            2.800000
Zepp            1.700000
N_exp_sig      55.854541
N_exp_bkg      52.922674
Sigma           5.360000
'''

'''
60 < Zmass < 120
Mjj          1100.000000
dEta            2.500000
Zepp            1.700000
N_exp_sig      58.867806
N_exp_bkg      64.682506
Sigma           5.300000
'''


Mjjcut  = 1100.000000
dEtacut = 2.500000
Zeppcut =  1.700000

# Confusion matrix
TP = sig_df.query('Mjj > @Mjjcut  and dEtajj > @dEtacut  and Zepp < @Zeppcut  and y > 0')['Mjj'].shape[0]
#FN = gen_sig - TP
FN = sel_sig - TP

FP_QCD120  = QCD120_df.query('Mjj > @Mjjcut  and dEtajj > @dEtacut  and Zepp < @Zeppcut  and y == 0')['Mjj'].shape[0]
FP_QCD600  = QCD600_df.query('Mjj > @Mjjcut  and dEtajj > @dEtacut  and Zepp < @Zeppcut  and y == 0')['Mjj'].shape[0]
FP_QCD1000  = QCD1000_df.query('Mjj > @Mjjcut  and dEtajj > @dEtacut  and Zepp < @Zeppcut  and y == 0')['Mjj'].shape[0]

FP = FP_QCD120+FP_QCD600+FP_QCD1000
#TN = gen_QCD120 + gen_QCD600 + gen_QCD1000 - FP
TN = sel_QCD120 + sel_QCD600 + sel_QCD1000 - FP

#TPR = TP / float(gen_sig)
TPR = TP / float(sel_sig)
#FPR = FP / float(gen_QCD120 + gen_QCD600 + gen_QCD1000)
FPR = FP / float(sel_QCD120 + sel_QCD600 + sel_QCD1000)
#ACC = (TP+TN) / float(gen_sig + gen_QCD120 + gen_QCD600 + gen_QCD1000)
ACC = (TP+TN) / float(sel_sig + sel_QCD120 + sel_QCD600 + sel_QCD1000)


print("TPR: ",round(TPR,3))
print("FPR: ",round(FPR,3))
print("ACC: ",round(ACC,3))

'''
('TPR: ', 0.259)
('FPR: ', 0.054)
('ACC: ', 0.606)
'''
