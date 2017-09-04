#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Created on Wed Jul 19 15:25:00 2017

@author: TristanSong
"""

import numpy as np
import time
from sklearn.ensemble import RandomForestClassifier

def loadTrainData(fileName, numThresh=50000):
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

def main():
    startTime = time.time()
    print('Reading train data...')
    X_train, y_train= loadTrainData('./train.csv')
    m, n = np.shape(X_train)
    print('Shape of train data: %d * %d'%(m, n))
    print('Reading train data complete!\n')

    print('Reading test data...')
    x_test = loadTestData('./test.csv')
    m, n = np.shape(x_test)
    print('Shape of test data: %d * %d'%(m, n))
    print('Reading test data complete!\n')

    print('Start train the data with Random Forest Classifier...')
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    print('Reading test data complete!\n')
    
    # check the accuracy of Random Forest model
##    print('Start predict the train data and verify the precision...')
##    predict = rf.predict(X_train[30000:, :])
##    predict = np.mat(predict).T
##    realVal = y_train[30000:, :]
##    totalNum = np.shape(predict)[0]
##    correct = len(np.nonzero((predict - realVal) == 0)[0])
##    accuracy = float(correct/totalNum)
##    print('The accuracy of the Random Forest model is: %.02f%%'%(100*accuracy))

    print('Start predict the test data...')
    rfPrediction = rf.predict(x_test)
    print('Predict complete!')

    print('Write the predict data to file...')
    with open('./RF_prediciton.csv', 'w') as f:
        f.write('ImageId,Label\n')
        for i in range(len(rfPrediction)):
            f.write('%d,%d\n'%(i+1, rfPrediction[i]))
    print('Writing complete!\n')    
    
    endTime = time.time()
    print('Time consumption: %.0f'%(endTime - startTime))

if __name__ == '__main__':
    main()
    
