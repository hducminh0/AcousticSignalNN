import numpy as np 
import scipy.io as sio
import h5py as hp 
from dim_reduction import svd_reduction

def bias(data):
# add bias terms to the first column of the data
	return np.insert(data, 0, 1, axis=1)

def split_set(signal, thickness):
# split the input data into training and testing set
	pos = round(len(signal) * 0.7)	# divide 70% of data as training set and the rest are for testing 
	training = {'signal': signal[0:pos, :], 'thickness': thickness[0:pos, :]}	# construct the training set, signal is the input data, thickness is the expected output
	testing = {'signal': signal[pos:, :], 'thickness': thickness[pos:, :]}	# construct the tetsting set
	return training, testing

def open_file(filename, signal, thickness):
# open the .mat file to extract the signal and thickness
# filename: name of file to be loaded
# signal: key of the signal array in the dictionary
# thickness: key of the thickness
	data = hp.File(filename)	
	signal = np.array(data[signal]).transpose()		# only take the real part of the signal as input 
	thickness = np.array(data[thickness]).transpose()
	return signal, thickness

def mse(approx, expected):
# mean square error
	return np.sum((approx - expected) ** 2, axis=0)/(len(expected))		# mse to see how well the model performs 
	
def import_raw(filename, signal = 'data/acc_signal', thickness = 'data/thickness'):
# load the raw data for dimension reduction and training
# filename: name of file to be loaded
# signal: key of the signal array in the dictionary
# thickness: key of the thickness
	signal, thickness = open_file(filename, signal, thickness)
	training, testing = split_set(signal, thickness)
	testing['signal'] = bias(testing['signal'])	
	training['signal'] = bias(training['signal'])	# add a bias column to the input signal
	return training, testing

def import_nn(filename, input_w = 'input_w', output_w = 'output_w'):
# import the trained network 
# filename: name of file to be loaded
# input_w: key of the input weight of the network 
# output_w: key of the output weight of the network 
	nn = sio.loadmat(filename)
	input_w = nn['input_w']
	output_w = nn['output_w']
	return input_w, output_w

def sigmoid(x):
	return 1/(1 + np.exp(x))

def hidden(signal, input_w):
# ha node in the hidden layer of the neural network 
# input_w: input weight of the hidden layer 
	return sigmoid(np.dot(signal, input_w))