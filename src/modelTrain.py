# -*- coding: utf-8 -*-

import dataPreprocess
import cnnModel

epoch = 35
dataType = 1
modelPath = 'dataType' + str(dataType) + '-epoch' + str(epoch) + '-size' + str(dataPreprocess.imgLength) + '.h5'


def train(x_train, y_train):
    x_train = cnnModel.preprocessImgData(x_train)
    y_train = cnnModel.toCategorical(y_train)
    cnnModel.train(x_train, y_train, epoch, modelPath)


def test(x_test, y_test):
    model = cnnModel.loadModelFromFile(modelPath)
    x_test = cnnModel.preprocessImgData(x_test)
    cnnModel.test(model, x_test, y_test, 50)


x_train, y_train = dataPreprocess.loadData(dataType)
train(x_train, y_train)
# test(x_test, y_test)
