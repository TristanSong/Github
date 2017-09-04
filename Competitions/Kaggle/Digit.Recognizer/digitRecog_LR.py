#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Created on Mon Jul 17 16:58:00 2017

@author: TristanSong
"""

import numpy as np
import time
import sys
import pickle

def loadTrainData(fileName, numThresh=11000):
    with open(fileName, 'r') as f:
        # ignore 1st line
        f.readline()
        X_train = []
        y_train = []
        num = 0
        for line in f.readlines():
            line = line.strip().split(',')
            dataArr = []
            if num >= numThresh:
                break
            for i in range(1, 785):
                if line[i] == '0':
                    dataArr.append(0)
                else:
                    dataArr.append(1)
            num += 1
            X_train.append(dataArr)
            y_train.append(int(line[0]))
    return np.mat(X_train), np.mat(y_train).T

def loadTestData(fileName, numThresh=30000):
    with open(fileName, 'r') as f:
        # ignore 1st line
        f.readline()
        x_test = []
        num = 0
        for line in f.readlines():
            line = line.strip().split(',')
            dataArr = []
            if num >= numThresh:
                break
            for i in range(784):
                if line[i] == '0':
                    dataArr.append(0)
                else:
                    dataArr.append(1)
            num += 1
            x_test.append(dataArr)
    return np.mat(x_test)

def sigmoid(inX):
    return 1.0/(1+np.exp(-inX))

def trainLogRegression(trainX, trainY, opts):
    m, n = np.shape(trainX)
    alpha = opts['alpha']
    maxIter = opts['maxIter']
    weights = np.ones((n, 1))

    for k in range(maxIter):
        # optimize through gradient descent algorithm
        if opts['optimizeType']=='gradDescent':
            output = sigmoid(trainX * weights)
            error = trainY - output
            weights = weights + alpha * trainX.transpose() * error
        
        # optimize through stochastic gradient descent
        elif opts['optimizeType']=='stocGradDescent':
            for i in range(m):
                output = sigmoid(trainX * weights)
                error = trainY - output
                weights = weights + alpha * trainX.transpose() * error  

        # optimize through smooth stochastic gradient descent
        elif opts['optimizeType']=='smoothStocGradDescent':
            dataIndex = list(range(m))
            for i in range(m):
                alpha = 4.0/(1+k) + 0.01
                randIndex = int(np.random.uniform(0, len(dataIndex)))
                output = sigmoid(trainX[dataIndex[randIndex], :] * weights)
                error = trainY[dataIndex[randIndex], 0] - output
                weights = weights + alpha * trainX[dataIndex[randIndex], :].transpose() * error
                del(dataIndex[randIndex])

        else:
            print('Not supported optimize method type!')
            sys.exit()

    return weights

def trainDigit(X_train, y_train, opts={'alpha': 0.01, 'maxIter': 50, 'optimizeType': 'smoothStocGradDescent'}):
    weights = {}
    for i in range(10):
        startTime = time.time()
        y_train_copy = y_train.copy()
        y_train_copy[np.nonzero(y_train_copy == i)] = i+10
        y_train_copy[np.nonzero(y_train_copy != i+10)] = 0
        y_train_copy[np.nonzero(y_train_copy == i+10)] = 1
        weight = trainLogRegression(X_train, y_train_copy, opts)
        weights[i] = weight
        endTime = time.time()
        print('Training Complete %d/10! Time consumption: %.0fs'%(i, endTime - startTime))     
    return weights

def lrAccuracy(x_test, y_test, weights):
    m = np.shape(x_test)[0]
    prediction = np.mat(np.zeros((m, 1)))
    output_base = np.mat(-np.ones((m, 1)))
    for i in range(10):
        output = sigmoid(x_test * weights[i])
        maxIndex = np.nonzero(output_base < output)
        output_base[maxIndex] = output[maxIndex]
        prediction[maxIndex] = i
    correctNum = len(np.nonzero((prediction - y_test) == 0)[0])
    return float(correctNum/m)

def predictDigit(x_test, weights):
    m = np.shape(x_test)[0]
    prediction = np.mat(np.zeros((m, 1)))
    output_base = np.mat(-np.ones((m, 1)))
    for i in range(10):
        output = sigmoid(x_test * weights[i])
        maxIndex = np.nonzero(output_base < output)
        output_base[maxIndex] = output[maxIndex]
        prediction[maxIndex] = i
    return prediction

def main():
    # reading the train data
##    print('Reading train data...')
##    X_train, y_train = loadTrainData('./train.csv')
##    X_train = np.insert(X_train, 0, values=1, axis=1)
##    m, n = np.shape(X_train)
##    print('Shape of train data: %d * %d'%(m, n))
##    print('Reading train data complete!\n')

    # reading the test data
    print('Reading test data...')
    x_test = loadTestData('./test.csv')
    x_test = np.insert(x_test, 0, values=1, axis=1)
    m, n = np.shape(x_test)
    print('Shape of test data: %d * %d'%(m, n))
    print('Reading test data complete!\n')

    # train the Logistic Regression model
##    print('Start training data set using Logistic Regression...')
##    weights = trainDigit(X_train[:10000, :], y_train[:10000, :])
##    weights_pkl = open('weights_pkl.pkl', 'wb')
##    pickle.dump(weights, weights_pkl)
##    weights_pkl.close()
##    print('Traing data set complete!')
    
    # check the accuracy of Logistic Regression model
##    print('Start checking the accurary...')
##    weights_pkl = open('weights_pkl.pkl', 'rb')
##    weights = pickle.load(weights_pkl)
##    accuracy = lrAccuracy(X_train[10000:, :], y_train[10000:, :], weights)
##    print('The accuracy of Logistic Regression model is: %.02f%%'%(100*accuracy))

    # predict the test data
    print('Start predict the test data...')
    weights_pkl = open('weights_pkl.pkl', 'rb')
    weights = pickle.load(weights_pkl)
    lrPrediction = predictDigit(x_test, weights)
    print('Prediction complete!')

    # write to files
    print('Write the results to file...')
    with open('./LR_prediciton.csv', 'w') as f:
        f.write('ImageId,Label\n')
        for i in range(np.shape(lrPrediction)[0]):
            f.write('%d,%d\n'%(i+1, lrPrediction[i, 0]))
    print('Writing complete!\n')

if __name__=='__main__':
    main()
