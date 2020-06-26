import h5py
import numpy as np
import argparse

def get_parser():
	parser = argparse.ArgumentParser(
		description='Run SUSY RPV training',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)
	parser.add_argument('--nb-train-events', action='store', type=int, default=999999999,
		help='Number of events to train on.')

	parser.add_argument('--nb-test-events', action='store', type=int, default=999999999,
		help='Number of events to test on.')
	
	parser.add_argument('--train_out_name', action='store', type=str, default='Preprocessed_train.h5',
		help='Output name for distributed train set.')
	
	parser.add_argument('--val_out_name', action='store', type=str, default='Preprocessed_val.h5',
		help='Output name for distributed train set.')
	
	parser.add_argument('--test_out_name', action='store', type=str, default='Preprocessed_test.h5',
		help='Output name for distributed train set.')

	parser.add_argument('--train_data', action='store', type=str,
		help='path to HDF5 file to train on')

	parser.add_argument('--val_data', action='store', type=str,
		help='path to HDF5 file to validate on')
	
	parser.add_argument('--test_data', action='store', type=str,
		help='path to HDF5 file to test on')

	parser.add_argument('--model', action='store', type=str,
		help='one of: "3ch-CNN", "CNN", "FCN", "BDT"')
	return parser

parser = get_parser()
args = parser.parse_args()



## --Parameter set
nb_train_events =  args.nb_train_events       
nb_test_events = args.nb_test_events		
modelName = args.model					#"3ch-CNN"  

## --Read data


##### Calculate Rescale factors ######
## -----------------------------------------------------##

##### Normed weight factors

print(" ######### Estimate Rescaling ######### ")
print(" #=========================================================# ")
print(" ")

Lumi		 = 150000
xsecSignal   = 0.013
xsecQCD120   = 1094.
xsecQCD600   = 99.16
xsecQCD1000  = 20.25

# Gen evts
GenSignal   = 1499322
GenQCD120	= 999986
GenQCD600	= 999986
GenQCD1000	= 999835

# weight = xsec * lumi / Gen evts
QCD120 = xsecQCD120 * Lumi / GenQCD120
QCD600 = xsecQCD600 * Lumi / GenQCD600
QCD1000 = xsecQCD1000 * Lumi / GenQCD1000
BKG_weight_sum  = QCD120 + QCD600 + QCD1000
print("## BKG weight sum {0}".format(BKG_weight_sum))

## Selected evts ( = # of DNN input )
Signal     = 170194
QCDsel120 = 56625
QCDsel600 = 56625
QCDsel1000 = 60368

## Renorm target ( signal selected evts )
target = Signal

##### Calculate scalefactor

# 1. Make w_QCD700+w_QCD1000+w_QCD1500+w_QCD2000 = 1
w_QCD120 = QCD120 / BKG_weight_sum
w_QCD600 = QCD600 / BKG_weight_sum
w_QCD1000 = QCD1000 / BKG_weight_sum

print("####   Normlaize weights to 0 ~ 1 ##")
print("## Normalized weight: ",w_QCD120+w_QCD600+w_QCD1000)
print(" ")

# 2. weight * selected evts
expQCD120 = w_QCD120 *QCDsel120
expQCD600 = w_QCD600 *QCDsel600
expQCD1000 = w_QCD1000 *QCDsel1000

print("####  Calculate expected evts ##")
print("#### Calcualte SF ##")
sf = expQCD120 + expQCD600 + expQCD1000
print("--> SF: {0}".format(sf))
print(" ")

expQCD120  = float(expQCD120 /sf)
expQCD600  = float(expQCD600 /sf)
expQCD1000  = float(expQCD1000 /sf)

print("####  Normalize expected evts ##")
print("Normalized expected evts {0}".format(expQCD120+expQCD600+expQCD1000))

##### Effective weight
# ----------------------------------------------#

w_QCD120 = w_QCD120 / sf *target
w_QCD600 = w_QCD600 / sf *target
w_QCD1000 = w_QCD1000 / sf *target



## -- print only ---->
print("### training effective  weight ###")
print("QCD120: {0}".format(w_QCD120))
print("QCD600: {0}".format(w_QCD600))
print("QCD1000: {0}".format(w_QCD1000))
print(" ")

print("### Effective events ###")
Eff_QCD120 = w_QCD120 * QCDsel120
Eff_QCD600 = w_QCD600 * QCDsel600
Eff_QCD1000 = w_QCD1000 * QCDsel1000

print("QCD120: {0}".format(Eff_QCD120))
print("QCD600: {0}".format(Eff_QCD600))
print("QCD1000: {0}".format(Eff_QCD1000))
print(" ")
print("### Sum of BKG effective evts(=signal selected evts)")
print(Eff_QCD120 + Eff_QCD600 + Eff_QCD1000)
print(" ")
print("### Signal selected evts)")
print(target)
print(" ")
## <------------ print only ----------------------




##### Start Rescaling ######
## -----------------------------------------------------##

# Initial weights (Fake)
Fw_signal  = 0.0012915837958757358
Fw_QCD120  = 0.07911110755550578
Fw_QCD600  = 0.004090557267801749
Fw_QCD1000 = 0.0013061155090589949


	#--Training
if (args.train_data != None):
	print(" ######### Start Rescaling..  ######### ")
	print(" #======================================================# ")
	print(" ")
	
	
	print(" ##### Start --> Training dataset #######" )
	data = h5py.File(args.train_data)
	print(list(data['all_events'].keys())) 
	images     = np.expand_dims(data['all_events']['hist'][:nb_train_events], -1)
	labels     = data['all_events']['y'][:nb_train_events]
	weights    = data['all_events']['weight'][:nb_train_events]
	
	
	# Shuffling
	NofData = data['all_events']['y'][:nb_train_events].shape[0]
	inds = np.arange(NofData)
	np.random.RandomState(11).shuffle(inds)
	images     = images[inds]
	labels     = labels[inds]
	weights    = weights[inds]
	
	print('## Signal ##')
	print("Initial_Signal_weight: ",Fw_signal) 
	dim_sig=weights[np.where(weights[:]==Fw_signal)].shape
	weights[np.where(weights[:]==Fw_signal)]=np.ones(dim_sig)
	
	print("## QCD 120-600 ##")
	print("Initial_QCD_120_weight: ",Fw_QCD120) 
	dim_QCD120 = weights[np.where(weights[:]==Fw_QCD120)].shape
	weights[np.where(weights[:] == Fw_QCD120)] = np.ones(dim_QCD120)*w_QCD120

	print("## QCD 600-1000 ##")
	print("Initial_QCD_600_weight: ",Fw_QCD600) 
	dim_QCD600 = weights[np.where(weights[:]==Fw_QCD600)].shape
	weights[np.where(weights[:] == Fw_QCD600)] = np.ones(dim_QCD600)*w_QCD600
	
	print("## QCD 1000-Inf ##")
	print("Initial_QCD_1000_weight: ",Fw_QCD1000) 
	dim_QCD1000 = weights[np.where(weights[:]==Fw_QCD1000)].shape
	weights[np.where(weights[:] == Fw_QCD1000)] = np.ones(dim_QCD1000)*w_QCD1000




	#--Validation
if (args.val_data != None):
	print(" ##### Start --> Validation dataset #######" )
	val = h5py.File(args.val_data)
	

	images_val = np.expand_dims(val['all_events']['hist'][:nb_test_events], -1)
	labels_val = val['all_events']['y'][:nb_test_events]
	weights_val = val['all_events']['weight'][:nb_test_events] 
	

	
	# Shuffling
	NofData = val['all_events']['y'][:nb_test_events].shape[0]
	inds = np.arange(NofData)
	np.random.RandomState(11).shuffle(inds)
	images_val     = images_val[inds]
	labels_val     = labels_val[inds]
	weights_val    = weights_val[inds]


	print('## Signal ##')
	print("Norm: ",Fw_signal) 
	dim_sig=weights_val[np.where(weights_val[:]==Fw_signal)].shape
	weights_val[np.where(weights_val[:]==Fw_signal)]=np.ones(dim_sig)
	
	print("## QCD 120-600 ##")
	print("Norm: ",Fw_QCD120) 
	dim_QCD120 = weights_val[np.where(weights_val[:]==Fw_QCD120)].shape
	weights_val[np.where(weights_val[:] == Fw_QCD120)] = np.ones(dim_QCD120)*w_QCD120
	
	print("## QCD 600-1000 ##")
	print("Norm: ",Fw_QCD600) 
	dim_QCD600 = weights_val[np.where(weights_val[:]==Fw_QCD600)].shape
	weights_val[np.where(weights_val[:] ==Fw_QCD600)] = np.ones(dim_QCD600)*w_QCD600
	
	print("## QCD 1000-Inf ##")
	print("Norm: ",Fw_QCD1000) 
	dim_QCD1000 = weights_val[np.where(weights_val[:]==Fw_QCD1000)].shape
	weights_val[np.where(weights_val[:] == Fw_QCD1000)] = np.ones(dim_QCD1000)*w_QCD1000


	#--Test
if (args.test_data != None):
	print(" ##### Start --> Test dataset #######" )
	test = h5py.File(args.test_data)
	images_test  = np.expand_dims(test['all_events']['hist'][:nb_test_events], -1)
	labels_test  = test['all_events']['y'][:nb_test_events]
	weights_test = test['all_events']['weight'][:nb_test_events] 
	#passSRJ =  test['all_events']['passSRJ'][:nb_test_events]
	
	
	# Shuffling
	NofData = test['all_events']['y'][:nb_test_events].shape[0]
	inds = np.arange(NofData)
	np.random.RandomState(11).shuffle(inds)
	images_test     = images_test[inds]
	labels_test     = labels_test[inds]
	weights_test    = weights_test[inds]
	#passSRJ = passSRJ[inds]
	
	print('## Signal ##')
	print("Norm: ",Fw_signal) 
	dim_sig=weights_test[np.where(weights_test[:]==Fw_signal)].shape
	weights_test[np.where(weights_test[:]==Fw_signal)]=np.ones(dim_sig)
	
	print("## QCD 120-600 ##")
	print("Norm: ",Fw_QCD120) 
	dim_QCD120 = weights_test[np.where(weights_test[:]==Fw_QCD120)].shape
	weights_test[np.where(weights_test[:] == Fw_QCD120)] = np.ones(dim_QCD120)*w_QCD120
	
	print("## QCD 600-1000 ##")
	print("Norm: ",Fw_QCD600) 
	dim_QCD600 = weights_test[np.where(weights_test[:]==Fw_QCD600)].shape
	weights_test[np.where(weights_test[:] == Fw_QCD600)] = np.ones(dim_QCD600)*w_QCD600
	
	print("## QCD 1000-Inf ##")
	print("Norm: ",Fw_QCD1000) 
	dim_QCD1000 = weights_test[np.where(weights_test[:]==Fw_QCD1000)].shape
	weights_test[np.where(weights_test[:] == Fw_QCD1000)] = np.ones(dim_QCD1000)*w_QCD1000
	



# -- 3ch-CNN case Merging
print(" ##### Start 3ch mergning #####" )
if modelName == '3ch-CNN':
	def add_channels(_images, _data, nb_events):
		layer_em = np.expand_dims(_data['all_events']['histEM'][:nb_events], -1)
		layer_track = np.expand_dims(_data['all_events']['histtrack'][:nb_events], -1)
		layer_em = layer_em / layer_em.max()
		layer_track = layer_track / layer_track.max()
		return np.concatenate((np.concatenate((_images,layer_em),axis=-1),layer_track),axis=-1)
	print("### 3ch merging")
	
	if (args.train_data != None):
		images 	  	= add_channels(images, data, nb_train_events)
	if (args.val_data != None):
		images_val  = add_channels(images_val, val, nb_test_events)
	if (args.test_data != None):
		images_test = add_channels(images_test, test, nb_test_events)
  	



print(" ##### Create hdf5 piles  #####" )
## -- Save the preprocessed data
if (args.train_data != None):
	print(" ## Create train.hdf5 ##" )
	with h5py.File(args.train_out_name,"w") as f:
		g=f.create_group("all_events")
		g.create_dataset("images", data=images,chunks=True,compression='gzip', compression_opts=9) ## Minimize output file size
		g.create_dataset("labels",data=labels,chunks=True)
		g.create_dataset("weights",data=weights,chunks=True)
		

if (args.val_data != None):
	print(" ## Create val.hdf5 ##" )
	with h5py.File(args.val_out_name,"w") as f:
		g=f.create_group("all_events")
		g.create_dataset("images_val", data=images_val,chunks=True,compression='gzip', compression_opts=9)
		g.create_dataset("labels_val",data=labels_val,chunks=True)
		g.create_dataset("weights_val",data=weights_val,chunks=True)
	

if (args.test_data != None):
	print(" ## Create test.hdf5 ##" )
	with h5py.File(args.test_out_name,"w") as f:
		g=f.create_group("all_events")
		g.create_dataset("images_val", data=images_test,chunks=True,compression='gzip', compression_opts=9)
		g.create_dataset("labels_val",data=labels_test,chunks=True)
		g.create_dataset("weights_val",data=weights_test,chunks=True)
#		g.create_dataset("passSRJ",data=passSRJ,chunks=True)
