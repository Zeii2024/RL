"""
A simple NN tackling MNIST with two layers
created at 20 Jan 2020

author @Terry
using tensorflow 1.14
"""
import keras
import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential, Model
from keras.utils import to_categorical
from keras.layers import Dense,Input, Embedding, LSTM
# import datasets
from tensorflow.examples.tutorials.mnist import input_data

# datasets
mnist = input_data.read_data_sets("MNIST_data/")
x_train = mnist.train.images
y_train = mnist.train.labels

x_test = mnist.test.images
y_test = mnist.test.labels

# initiate a Sequential
model = Sequential()

# create network # two layers
# add a dense cosisted of 784 inputs and 784 outputs with activation 'relu'
model.add(Dense(units=784, activation='relu', input_dim=784))

# add a dense cosisted of 10 outputs with 'softmax'
model.add(Dense(units=10, activation='softmax'))

# check the params of model by Summary
# before this in first layer input_shape (input_dim) must be specified
# model.summary() 

# compile the model by Compile
model.compile(loss='categorical_crossentropy', # loss function: crossentropy
                optimizer='sgd',               # optimizer 
                metrics=['accuracy'])          # performance evaluation

# Train
# convert y to one-hot
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# train the model
model.fit(x_train, y_train, epochs=5, batch_size=32)

# evaluate the model
score = model.evaluate(x_test, y_test, batch_size=128)
print("loss: ", score[0])
print("accu: ", score[1])
