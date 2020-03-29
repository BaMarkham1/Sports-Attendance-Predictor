# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 17:24:31 2020

@author: lemar
"""
import pandas as pd
import numpy as np



probowl_count = pd.read_csv("csvs/probowl_data.csv", index_col=["year", "team"])
team_record = pd.read_csv("csvs/team_record_data.csv", index_col=["year", "team"])
attendance = pd.read_csv("csvs/attendance_data.csv", index_col=["year", "team"])

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
        
def remove_blanks(df):
    df.replace('', np.nan, inplace=True)
    df = df.dropna()
    return df
    
           


    

merged_table = merge_data(probowl_count, team_record, attendance)
next_year_df = get_diff_season_stats(merged_table, ["attend%", "attendance"], 1)
next_year_df = remove_blanks(next_year_df)
next_year_df.to_csv("csvs/next_season.csv")
