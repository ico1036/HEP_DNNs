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

	print(" ---- START data loading ---- ")
	
	path='../data/data_normal_by_all/'
	
	# read data
	train_data = pd.read_csv(path+'train_data.csv', sep=',')
	val_data   = pd.read_csv(path+'val_data.csv', sep=',')
	test_data  = pd.read_csv(path+'test_data.csv', sep=',')
	
	
	train_data.pop('dEtaJJ')
	val_data.pop('dEtaJJ')
	test_data.pop('dEtaJJ')

	train_data.pop('mJJ')
	val_data.pop('mJJ')
	test_data.pop('mJJ')


	display(test_data.describe())

	train_data.hist(bins=50, figsize=(20,15))
	plt.savefig('features.png')



	y_train = train_data.pop('issig')
	x_train = train_data
	
	y_val = val_data.pop('issig')
	x_val = val_data
	
	y_test = test_data.pop('issig')
	x_test = test_data
	
	print(" ")
	print(" ---- END data loading ---- ")
	
	print(x_train.shape)
	print(x_val.shape)
	print(x_test.shape)
	print(" ")	

	# HyperParameter
	batch_size = args.batch
	training_epochs= args.epoch
	neu = args.neurons
	
	## --Model
	x = layers.Input(shape=[len(x_train.keys())])
	
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

	# --layer4
	h = layers.Dense(neu, activation='relu')(h)
	h = layers.Dropout(0.5)(h)
	h = layers.BatchNormalization()(h)	

	# --layer5
	h = layers.Dense(neu, activation='relu')(h)
	h = layers.Dropout(0.5)(h)
	h = layers.BatchNormalization()(h)	
	
	y = layers.Dense(1, activation='sigmoid')(h)
	model = tf.keras.Model(inputs = x,outputs = y)
	model.summary()
	model.compile(optimizer='adam',
	    loss='binary_crossentropy',
	    metrics=['accuracy']
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
	    model.fit(x_train, y_train,
	        batch_size=batch_size,
	        epochs=training_epochs,
	        verbose=1,
	        callbacks = [
	            tf.keras.callbacks.EarlyStopping(verbose=True, patience=10, monitor='val_loss'),
	            tf.keras.callbacks.ModelCheckpoint(model_weights,
	            monitor='val_loss', verbose=True, save_best_only=True),
				csv_logger
	        ],
	        validation_data=(x_val, y_val)
	    )
	except KeyboardInterrupt:
	    print('Training finished early')
	
	model.load_weights(model_weights)
	yhat = model.predict(x_test, verbose=1, batch_size=batch_size)
	       # score = model.evaluate(images_val, labels_val, sample_weight=weights_val, verbose=1)
	       # print 'Validation loss:', score[0]
	       # print 'Validation accuracy:', score[1]
	np.save(predictions_file, yhat)
	
	test_loss, test_acc = model.evaluate(x_test,y_test)
	print('test_acc: ', test_acc)

