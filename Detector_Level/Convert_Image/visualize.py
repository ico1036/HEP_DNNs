import h5py

import numpy as np
import sys
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('path', type=str,
            help="import filepath")

args = parser.parse_args()

data = h5py.File(args.path)
print(data['all_events'].keys())
weights = data['all_events']['weight'][:]
print(weights)


images = data['all_events']['hist'][:]
images_em = data['all_events']['histEM'][:]
images_track = data['all_events']['histtrack'][:]
labels = data['all_events']['y'][:]
labels=labels.flatten()



### ---- M A K E   P L O T -------------------

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

matplotlib.rcParams.update({'font.size': 20})


def plot_image(image,name="BKG.png"):

	fig = plt.figure(figsize=(10,10))
	im = plt.imshow(image,
	           interpolation='nearest',
	           #norm=LogNorm(vmin, vmax)
	)
	cbar = plt.colorbar(fraction=0.0455)
	#cbar.set_label(r'Energy (MeV)', y=0.83)
	cbar.ax.tick_params()   
	plt.ylabel(r'$\eta$ Cell ID')
	plt.xlabel(r'$\phi$ Cell ID')
	plt.tight_layout()
	plt.savefig(name)
	return im


plot_image((weights.reshape(-1, 1, 1)*images)[labels==1].mean(axis=0),"Signal_image_HCAL.png")
plot_image((weights.reshape(-1, 1, 1)*images_em)[labels==1].mean(axis=0),"Signal_image_ECAL.png")
plot_image((weights.reshape(-1, 1, 1)*images_track)[labels==1].mean(axis=0),"Signal_image_Track.png")

plot_image((weights.reshape(-1, 1, 1)*images)[labels==0].mean(axis=0),"BKG_image_HCAL.png")
plot_image((weights.reshape(-1, 1, 1)*images_em)[labels==0].mean(axis=0),"BKG_image_ECAL.png")
plot_image((weights.reshape(-1, 1, 1)*images_track)[labels==0].mean(axis=0),"BKG_image_Track.png")


plot_image((weights.reshape(-1, 1, 1)*images)[labels==1][0],"Signal_sample_HCAL.png")
plot_image((weights.reshape(-1, 1, 1)*images)[labels==0][0],"BKG_sample_HCAL.png")




#plot_image((weights.reshape(-1, 1, 1)*images)[labels==1].mean(axis=0),"noPU_HCAL_SIG.png")
#plot_image((weights.reshape(-1, 1, 1)*images_em)[labels==0].mean(axis=0),"noPU_ECAL_BKG.png")
#plot_image((weights.reshape(-1, 1, 1)*images_em)[labels==1].mean(axis=0),"noPU_ECAL_SIG.png")
#plot_image((weights.reshape(-1, 1, 1)*images_track)[labels==0].mean(axis=0),"noPU_Track_BKG.png")
#plot_image((weights.reshape(-1, 1, 1)*images_track)[labels==1].mean(axis=0),"noPU_Track_SIG.png")
#plot_image((weights.reshape(-1, 1, 1)*images_track_pt)[labels==0].mean(axis=0),"noPU_TrackPT_BKG.png")
#plot_image((weights.reshape(-1, 1, 1)*images_track_pt)[labels==1].mean(axis=0),"noPU_TrackPT_SIG.png")








