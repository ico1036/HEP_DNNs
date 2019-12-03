import tensorflow as tf
import numpy as np
import random
import matplotlib
import pandas as pd
from IPython.display import display
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--batch', type=int, default=512,
            help="--batch 'batch size'")
parser.add_argument('--epoch', type=int, default=50,
            help="--epoch 'training epoch'")
parser.add_argument('--neurons', type=int, default=512,
            help="--neurons 'N of neurons per layer' ")

args = parser.parse_args()



if __name__ == '__main__':
	
	### --- Split labels and Features
	
	train_data = pd.read_csv('data/train_data.csv', sep=',')
	val_data   = pd.read_csv('data/val_data.csv'  , sep=',')
	test_data  = pd.read_csv('data/test_data.csv' , sep=',')
	
	train_labels = train_data.pop('l2Eta')
	val_labels   = val_data.pop('l2Eta')
	test_labels  = test_data.pop('l2Eta')
	
	# HyperParameter
	batch_size = args.batch
	training_epochs= args.epoch
	neu = args.neurons


	### --- Normalize data
	
	# --MinMaxScaler
	def MinMaxScaler(data):
		numerator = data - np.min(data,0)
		denominator = np.max(data,0) - np.min(data,0)
		denominator = denominator.astype('float')
		return numerator / denominator
	
	def Zscore(data):
		return( (data - np.mean(data)) / np.std(data) )

	test_data.hist(bins=50, figsize=(20,15))
	plt.savefig('originhist.png')


	# --Do norm
	norm=True
	if norm:
		train_data = MinMaxScaler(train_data)
		val_data   = MinMaxScaler(val_data)
		test_data  = MinMaxScaler(test_data)
	
	test_data.hist(bins=50, figsize=(20,15))
	plt.savefig('normedhist.png')

	
	### --- Model
	
	
	# --Input
	x = layers.Input(shape=[len(train_data.keys())])
	
	# --layer1
	h = layers.Dense(neu, activation='relu')(x)
	h = layers.Dropout(0.5)(h)
	h = layers.BatchNormalization()(h)
	
	# --layer2
	h = layers.Dense(neu, activation='relu')(h)
	h = layers.Dropout(0.5)(h)
	h = layers.BatchNormalization()(h)
	
	# --layer3
	h = layers.Dense(neu, activation='relu')(h)
	h = layers.Dropout(0.5)(h)
	h = layers.BatchNormalization()(h)
	
	
# --OUtput
	y = layers.Dense(1, activation='relu')(h)
	
	adam = tf.keras.optimizers.Adam(lr=0.001)
	model = tf.keras.Model(inputs = x,outputs = y)
	model.summary()
	model.compile(optimizer=adam,
	    loss='mse',
	    metrics=['mse']
	)
	
	model_weights = 'model_weights_log.h5'
	predictions_file = 'prediction_nn_log.pyc'
	
	# --Training monitoring
	from keras.callbacks import CSVLogger
	csv_logger = CSVLogger('train_log.csv', append=True, separator=',')
	
	try:
	    model.load_weights(model_weights)
	    print('Weights loaded from ' + model_weights)
	except IOError:
	    print('No pre-trained weights found')
	try:
	    model.fit(train_data,train_labels,
	        batch_size=batch_size,
	        epochs=training_epochs,
	        verbose=1,
	        callbacks = [
	            tf.keras.callbacks.EarlyStopping(verbose=True, patience=10, monitor='val_loss'),
	            tf.keras.callbacks.ModelCheckpoint(model_weights,
	            monitor='val_loss', verbose=True, save_best_only=True),
	            csv_logger
	        ],
	        validation_data=(val_data, val_labels)
	    )
	except KeyboardInterrupt:
	    print('Training finished early')
	
	model.load_weights(model_weights)
	yhat = model.predict(test_data, verbose=1, batch_size=batch_size)
	np.save(predictions_file, yhat)
	

	np.savetxt('prediction.csv',yhat,delimiter=',')

	test_loss, test_acc = model.evaluate(test_data,test_labels)
	print('test_loss: ', test_loss)

