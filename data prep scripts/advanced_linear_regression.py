# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA

def prepare_x_y(dataset, target_column, columns_to_drop):
    #get the target column to predict
    y = dataset[target_column].to_numpy()
    #get all the current columns
    x_columns = list(dataset.columns)
    #drop the columns we don't want to use as independent variables
    x_columns.remove(target_column)
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

def get_train_and_test_sets(splits, test_index):
    train_list = splits.copy()
    del train_list[test_index]
    train = np.concatenate(train_list, axis=0)
    test = splits[test_index].copy()
    return train, test

def cross_validation(x, y, num_of_folds):
    total_pred_list = []
    total_actual_list = []
    x_splits = np.array_split(x, num_of_folds)
    y_splits = np.array_split(y, num_of_folds)
    for split_index in range(num_of_folds):
        x_train, x_test = get_train_and_test_sets(x_splits, split_index)
        y_train, y_test = get_train_and_test_sets(y_splits, split_index)
        y_pred = do_linear_regression(x_train, x_test, y_train)
        #get the correlation between predicted and actual values
        print(np.corrcoef(y_test, y_pred)[0][1])
        total_pred_list.extend(y_pred.tolist())
        total_actual_list.extend(y_test.tolist())
    total_pred = np.asarray(total_pred_list)
    total_actual = np.asarray(total_actual_list)
    return np.corrcoef(total_actual, total_pred)[0][1]
    
    
#read in the dataset
dataset = pd.read_csv("../csvs/full_dataset.csv")
#list columns to not be an x
x_columns_to_drop = ["year", "team", "year 1 attend%", "attend%", "attendance"]
x, y = prepare_x_y(dataset, "year 1 attendance", x_columns_to_drop)
print(cross_validation(x, y, 5))


