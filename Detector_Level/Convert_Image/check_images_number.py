import h5py
import glob

Files_Signal  = glob.glob("outimages/Signal*.h5")
Files_QCD120  = glob.glob("outimages/QCD120*.h5")
Files_QCD600  = glob.glob("outimages/QCD600*.h5")
Files_QCD1000 = glob.glob("outimages/QCD1000*.h5")


sum_signal=0
for f in Files_Signal:
	dat = h5py.File(f,'r')
	sum_signal += dat['all_events']['weight'][:].shape[0]
	dat.close()
print(sum_signal)


sum_QCD120=0
for f in Files_QCD120:
	dat = h5py.File(f,'r')
	sum_QCD120 += dat['all_events']['weight'][:].shape[0]
	dat.close()
print(sum_QCD120)


sum_QCD600=0
for f in Files_QCD600:
	dat = h5py.File(f,'r')
	sum_QCD600 += dat['all_events']['weight'][:].shape[0]
	dat.close()
print(sum_QCD600)

sum_QCD1000=0
for f in Files_QCD1000:
	dat = h5py.File(f,'r')
	sum_QCD1000 += dat['all_events']['weight'][:].shape[0]
	dat.close()
print(sum_QCD1000)
