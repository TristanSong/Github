#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Created on Thur Jul 20 15:07:00 2017

@author: TristanSong
"""

import numpy as np
from sklearn.svm import SVC
import time

def loadTrainData(fileName, numThresh=30000):
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
    # reading the train data
    print('Reading train data...')
    X_train, y_train = loadTrainData('./train.csv')
    X_train = np.insert(X_train, 0, values=1, axis=1)
    m, n = np.shape(X_train)
    print('Shape of train data: %d * %d'%(m, n))
    print('Reading train data complete!\n')

    # reading the test data
    print('Reading test data...')
    x_test = loadTestData('./test.csv')
    x_test = np.insert(x_test, 0, values=1, axis=1)
    m, n = np.shape(x_test)
    print('Shape of test data: %d * %d'%(m, n))
    print('Reading test data complete!\n')

    print('Start train the SVM model...')
    clf = SVC()
    clf.fit(X_train, y_train)
    print('SVM model training complete!')

##    print('Start checking the accurary...')
##    predict = clf.predict(X_train[10000:, :])
##    predict = np.mat(predict).T
##    realVal = y_train[10000:, :]
##    totalNum = np.shape(predict)[0]
##    correct = len(np.nonzero(realVal == predict)[0])
##    accuracy = float(correct/totalNum)
##    print('The accuracy of the SVM model is: %.02f%%'%(100*accuracy))

    print('Start predict the test data...')
    svmPrediction = clf.predict(x_test)
    print('Predict complete!')

    print('Write the predict data to file...')
    with open('./svm_prediciton.csv', 'w') as f:
        f.write('ImageId,Label\n')
        for i in range(len(svmPrediction)):
            f.write('%d,%d\n'%(i+1, svmPrediction[i]))
    print('Writing complete!\n')    

    endTime = time.time()
    print('Time consumption is: %.fs'%(endTime-startTime))

if __name__ == '__main__':
    main()
