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
sig_df	   = sig_df.drop(sig_df[(sig_df['eeM'] < 60) | (sig_df['eeM'] > 120)].index)
QCD120_df  = QCD120_df.drop(QCD120_df[(QCD120_df['eeM'] < 60) | (QCD120_df['eeM'] > 120)].index)
QCD600_df  = QCD600_df.drop(QCD600_df[(QCD600_df['eeM'] < 60) | (QCD600_df['eeM'] > 120)].index)
QCD1000_df = QCD1000_df.drop(QCD1000_df[(QCD1000_df['eeM'] < 60) | (QCD1000_df['eeM'] > 120)].index)


xsec_sig = 0.01291
xsec_QCD120 = 0.5274
xsec_QCD600 = 0.02727
xsec_QCD1000 = 0.008706


gen_sig = 1499322.
gen_QCD120 = 999986.
gen_QCD600 = 999986.
gen_QCD1000 = 999835.



# --Optimize cut ranges
Domain_Mjj  = [500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500]
Domain_dEta = list([round(i*0.1,1) for i in range(0,60)])
Domain_zepp = list([round(i*0.1,1) for i in range(0,50)])
Domain_zepp.reverse()

print("Mjj  dEta Zepp N_exp_sig N_exp_bkg Sigma")
for i in range(len(Domain_Mjj)):

	for j in range(len(Domain_dEta)):

		for k in range(len(Domain_zepp)):
			

			N_sig   =sig_df.query('Mjj > @Domain_Mjj[@i] and dEtajj > @Domain_dEta[@j] and Zepp < @Domain_zepp[@k] and y > 0')['Mjj'].shape[0]
			N_exp_sig = N_sig * xsec_sig / gen_sig * Lumi			

			N_QCD120   =QCD120_df.query('Mjj > @Domain_Mjj[@i] and dEtajj > @Domain_dEta[@j] and Zepp < @Domain_zepp[@k] and y == 0')['Mjj'].shape[0]
			N_exp_QCD120 = N_QCD120 * xsec_QCD120 / gen_QCD120 * Lumi			

			N_QCD600   =QCD600_df.query('Mjj > @Domain_Mjj[@i] and dEtajj > @Domain_dEta[@j] and Zepp < @Domain_zepp[@k] and y == 0')['Mjj'].shape[0]
			N_exp_QCD600 = N_QCD600 * xsec_QCD600 / gen_QCD600 * Lumi			
			
			N_QCD1000   =QCD1000_df.query('Mjj > @Domain_Mjj[@i] and dEtajj > @Domain_dEta[@j] and Zepp < @Domain_zepp[@k] and y == 0')['Mjj'].shape[0]
			N_exp_QCD1000 = N_QCD1000 * xsec_QCD1000 / gen_QCD1000 * Lumi			
			
			N_exp_bkg = N_exp_QCD120 + N_exp_QCD600 + N_exp_QCD1000



			if(N_exp_sig+N_exp_bkg ==0):
				continue;
			Sigma = N_exp_sig / math.sqrt( N_exp_sig+N_exp_bkg )
			print(Domain_Mjj[i],Domain_dEta[j],Domain_zepp[k],N_exp_sig,N_exp_bkg,round(Sigma,2))













