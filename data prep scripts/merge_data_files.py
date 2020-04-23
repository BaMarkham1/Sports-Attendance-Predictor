# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 17:24:31 2020

@author: lemar
"""
import pandas as pd
import numpy as np



probowl_count = pd.read_csv("../csvs/probowl_data.csv", index_col=["year", "team"])
team_record = pd.read_csv("../csvs/team_record_data.csv", index_col=["year", "team"])
attendance = pd.read_csv("../csvs/attendance_weather_data.csv", index_col=["year", "team"])

def merge_data(probowl_count, team_record, attendance):
    merged_table = pd.merge(probowl_count, team_record, how="left", left_index = True ,right_index=True)
    merged_table = pd.merge(merged_table, attendance, how="left", left_index = True ,right_index=True)
    return merged_table

def get_diff_season_stats(df, stat_list, direction):
    for index, row in df.iterrows():
        match_index = (index[0] + direction, index[1])
        if match_index in df.index:
            for stat in stat_list: 
                df.at[index, "year " + str(direction) + " " + stat] = df.at[match_index, stat]
    return df


#Subtract the mean from each value and divide the result by the std deviation of the column
def normalize_data(data_array):
    mean_array = np.mean(data_array, axis = 0)
    std_array = np.std(data_array, axis = 0)
    normalized_array = np.zeros(data_array.shape)
    for col_index, col in enumerate(mean_array):
        mean = mean_array[col_index]
        std = std_array[col_index]
        normalized_array[:,col_index] = (data_array[:,col_index] - mean) / std
    return normalized_array
        
def remove_blanks(df):
    df.replace('', np.nan, inplace=True)
    df = df.dropna()
    return df
    
def normalize_table(df):
    #print(df.mean())
    print(df.std())
    normalized_df=(df-df.mean())/df.std()
    columns_to_keep = ["attendance", "attend%", "year 1 attend%", "year 1 attendance"]
    for col in columns_to_keep:
        normalized_df[col] = df[col]
    return normalized_df
    

merged_table = merge_data(probowl_count, team_record, attendance)
next_year_df = get_diff_season_stats(merged_table, ["attend%", "attendance"], 1)
next_year_df = remove_blanks(next_year_df)
next_year_df = normalize_table(next_year_df)
next_year_df.to_csv("../csvs/full_dataset.csv")
normalize_table(next_year_df).to_csv("../csvs/normalized.csv")