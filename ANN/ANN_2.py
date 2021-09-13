#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 13:58:35 2021

@author: surbhi

ANN_2.py - has been trained on all data (without splitting) and has been tested on validation data with 142 molecules, to get the final predictions of molecules.

"""


import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import confusion_matrix, accuracy_score


#file_validation = 'Datasets/Validation2_142.csv'
#file_datasheet = 'Datasets/90.51_Sheet_192.csv'
file_validation = '../DataSheets/Validation2_142.csv'
file_datasheet = '../DataSheets/90.51_Sheet_192.csv' #shuffled

def fetchDataset(sheet,cols):
    dataset11 = pd.read_csv(sheet)
    dataset = dataset11[cols]
    dataset.head()
    return dataset


def handleMissingValues(X):
    #handle missing values and replace with mean values
    imputer = SimpleImputer(missing_values = np.nan, strategy = 'mean')
    imputer = imputer.fit(X)
    X = imputer.transform(X)
    return X


def splitDatasetToTrainTest(X,Y):
    #split data into Training data and Test data
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)
    return X_train,X_test,Y_train,Y_test


def featureScaleDataSet(train,test):
    sc_X = StandardScaler()
    train = sc_X.fit_transform(train)
    test = sc_X.transform(test)
    return sc_X,train,test


def scaleSet(train):
    sc_X = StandardScaler()
    train = sc_X.fit_transform(train)
    return sc_X,train






if __name__=="__main__":
    print('\nStarting Execution')
    
    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    #working on Training dataset - fetch and split data
    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    dataset = fetchDataset(file_datasheet,['Index','C Log P','TPSA','Molecular Weight','nON','nOHNH','ROTB','Molecular Volume','Decision'])
    X = dataset.iloc[:,1:-1].values
    Y = dataset.iloc[:, -1:].values
    
    #fetch testing data from validation sheet
    dataset = fetchDataset(file_validation,['Index','C Log P','TPSA','Molecular Weight','nON','nOHNH','ROTB','Molecular Volume'])
    X_test = dataset.iloc[:,1:].values
    
    
    #handle missing values and replace with mean value in train data
    X = handleMissingValues(X)
    X_test = handleMissingValues(X_test)
    
    #feature scale train data
    sc_X, X = scaleSet(X)
    sc_XT, X_test = scaleSet(X_test)
    
    #initialize ANN
    classifier = Sequential()
    
    #add input layer and first hidden layer
    classifier.add(Dense(6, activation = 'relu', input_dim = 7))
    
    #adding 2nd hidden layer
    classifier.add(Dense(6, activation = 'relu'))
    
    #add output layer
    classifier.add(Dense(1, activation = 'sigmoid'))
    
    #train the model
    classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    classifier.fit(X, Y, batch_size = 10, epochs=100)
    
    #predict values
    Y_pred = classifier.predict(X_test)
    Y_pred = (Y_pred > 0.5)
    
    #confusion matrix
    print("Y_pred : \n",Y_pred)
