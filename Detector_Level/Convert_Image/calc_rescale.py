import h5py
import numpy as np
import argparse


## --Read data


##### Calculate Rescale factors ######
## -----------------------------------------------------##

##### Normed weight factors

print(" ######### Estimate Rescaling ######### ")
print(" #=========================================================# ")
print(" ")


Lumi		 = 150000
xsecSignal   = 0.01291
xsecQCD120   = 0.5274
xsecQCD600   = 0.02727
xsecQCD1000  = 0.008706

# Gen evts
GenSignal   = 1499322
GenQCD120	= 999986
GenQCD600	= 999986
GenQCD1000	= 999835

# weight = xsec * lumi / Gen evts
Signal = xsecSignal * Lumi / GenSignal
QCD120 = xsecQCD120 * Lumi / GenQCD120
QCD600 = xsecQCD600 * Lumi / GenQCD600
QCD1000 = xsecQCD1000 * Lumi / GenQCD1000
BKG_weight_sum  = QCD120 + QCD600 + QCD1000
print("## BKG weight sum {0}".format(BKG_weight_sum))


## Selected evts ( = # of DNN input )
Signalsel     = 170194
QCDsel120 = 56625
QCDsel600 = 56625
QCDsel1000 = 60368


print(" ")
print("Default weights and Expected events ###")
print(Signal, Signal*Signalsel)
print(QCD120, QCD120*QCDsel120)
print(QCD600, QCD600*QCDsel600)
print(QCD1000, QCD1000*QCDsel1000)
print(" ")

## Renorm target ( signal selected evts )
target = Signalsel

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
Norm_sig = 827.71
Norm_QCD120 = 69654980.
Norm_QCD600 = 6313517.2
Norm_QCD1000 = 1289317.5
