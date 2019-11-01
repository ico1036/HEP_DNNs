import tensorflow as tf
import numpy as np
import random
import matplotlib
import pandas as pd
from IPython.display import display
from tensorflow import keras
from tensorflow.keras import layers

if __name__ == '__main__':

	print(" ---- START data loading ---- ")
	path='../data/'
	# read data
	train_data = np.loadtxt(path+'train_data.csv', delimiter=',')
	val_data   = np.loadtxt(path+'val_data.csv', delimiter=',')
	test_data  = np.loadtxt(path+'test_data.csv', delimiter=',')
	
	x_train = train_data[:,:-1]
	y_train = train_data[:,-1]
	
	x_val = val_data[:,:-1]
	y_val = val_data[:,-1]
	
	x_test = test_data[:,:-1]
	y_test = test_data[:,-1]
	
	print(" ")
	print(" ---- END data loading ---- ")
	
	print(x_train.shape)
	print(x_val.shape)
	print(x_test.shape)
	print(" ")	

	# HyperParameter
	batch_size = 512
	training_epochs=20
	neu = 64
	
	## --Model
	x = layers.Input(shape=(9,))
	
	h = layers.Dense(neu, activation='relu')(x)
	h = layers.Dropout(0.7)(h)
	h = layers.BatchNormalization()(h)	

	h = layers.Dense(neu, activation='relu')(x)
	h = layers.Dropout(0.7)(h)
	h = layers.BatchNormalization()(h)	

	h = layers.Dense(neu, activation='relu')(x)
	h = layers.Dropout(0.7)(h)
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
	            tf.keras.callbacks.EarlyStopping(verbose=True, patience=8, monitor='val_loss'),
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


