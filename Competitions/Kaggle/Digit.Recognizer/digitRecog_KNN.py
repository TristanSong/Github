#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Create on Fri Jul 14 11:25:00 2017

@author: TristanSong
"""
# kNN algorithm
import numpy as np
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
    return np.mat(X_train), np.mat(y_train)

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

def knnClassify(inX, X_train, y_train, k):
    y_train = y_train.A.flatten()
    m = np.shape(X_train)[0]
    diffMat = np.tile(inX, (m, 1)) - X_train
    sqDiffMat = np.power(diffMat, 2)
    sqDistances = np.sum(sqDiffMat, axis=1)
    distances = np.power(sqDistances, 0.5)
    sortedDistInd = np.argsort(distances.A.flatten())
    classCount = {}
    for i in range(k):
        vote = y_train[sortedDistInd[i]]
        classCount[vote] = classCount.get(vote, 0) + 1
    return max(classCount.items(), key=lambda x: x[1])[0]

def accuracy(prediction, test):
    length = np.shape(prediction)[1]
    n = 0
    for i in range(length):
        if prediction[0, i] == test[0, i]:
            n += 1
    return float(n/length)

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

    print('KNN classify starts...')
    knnPrediction = []
    totalNum = np.shape(x_test)[0]
    for i in range(totalNum):
        if i % 100 == 0:
            print('Classify complete %.02f%%...'%(100*i / totalNum))
        prediction = knnClassify(x_test[i, :], X_train, y_train, 5)
        knnPrediction.append(prediction)
    knnPrediction = np.mat(knnPrediction)
    print('KNN classify complete!')
##    precision = accuracy(knnPrediction, y_train)
##    print('The KNN classify accuracy is: %.02f%%'%(100*precision))

    print('Write the results to file...')
    with open('./kNN_prediciton.csv', 'w') as f:
        f.write('ImageId,Label\n')
        for i in range(np.shape(knnPrediction)[1]):
            f.write('%d,%d\n'%(i+1, knnPrediction[0, i]))
    print('Writing complete!\n')

    endTime = time.time()
    print('Time consumption: %.0f'%(endTime - startTime))
##    time consumption: 6506s
 
if __name__ == '__main__':
    main()
