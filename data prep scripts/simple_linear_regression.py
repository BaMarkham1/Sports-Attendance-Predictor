# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 16:07:48 2020

@author: lemar
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression

def prepare_x_y(target_column, columns_to_drop):
    #get the target column to predict
    y = dataset["year 1 attendance"].to_numpy()
    #get all the current columns
    x_columns = list(dataset.columns)
    #drop the columns we don't want to use as independent variables
    
    for col in columns_to_drop:
        x_columns.remove(col)
    #get a numpy array from the dataframe
    x = dataset[x_columns].to_numpy()
    return x, y

def do_linear_regression(x_train, x_test, y_train):
    #do the linear regression
    regressor = LinearRegression()  
    regressor.fit(x_train, y_train)
    #predict based on the training data
    y_pred = regressor.predict(x_test)
    return y_pred

#read in the dataset
dataset = pd.read_csv("../csvs/full_dataset.csv")
#list columns to not be an x
columns_to_drop = ["year", "team", "year 1 attendance", "year 1 attend%", "attend%"]
x, y = prepare_x_y("year 1 attendance", columns_to_drop)
#split the data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
y_pred = do_linear_regression(x_train, x_test, y_train)
#get the correlation between predicted and actual values
print(np.corrcoef(y_test, y_pred)[0][1])
    
