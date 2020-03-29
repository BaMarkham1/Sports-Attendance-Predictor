# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:12:02 2020

@author: lemar
"""

import pandas as pd

#list of the abbreviations PFR.com uses for each team
team_list = [
                "crd" , 
                "atl" , 
                "rav" ,
                "buf" ,
                "car" ,
                "chi" ,
                "cin" ,
                "cle" ,
                "dal" ,
                "den" ,
                "det" ,
                "gnb" ,
                "htx" ,
                "clt" ,
                "jax" ,
                "kan" ,
                "sdg" ,
                "ram" ,
                "mia" ,
                "min" ,
                "nwe" ,
                "nor" ,
                "nyg" ,
                "nyj" ,
                "rai" ,
                "phi" ,
                "pit" ,
                "sfo" ,
                "sea" ,
                "tam" ,
                "oti" ,
                "was" , 
            ]

numeric_dict = { "1st of 4" : 1 , "2nd of 4" : 2, "3rd of 4" : 3, "4th of 4" : 4, "Lost WC" : 2, "Lost Div" : 3, "Lost Conf" : 4, "Lost SB" : 5, "Won SB" : 6, 1 : 1 }

#tables = pd.read_html("https://www.pro-football-reference.com/teams/nwe/")
#for each in tables:
#    print(each)

url_prefix = "https://www.pro-football-reference.com/teams/"


def get_data():
    main_table = pd.DataFrame()
    for team_abbr in team_list:
        #print(team_abbr)
        team_table = pd.read_html(url_prefix + team_abbr + "/")[0]
        team_table = team_table.head(14)
        team_table = team_table[[('Unnamed: 0_level_0', 'Year'), ('Unnamed: 3_level_0', 'W'), ('Unnamed: 4_level_0', 'L'), ('Unnamed: 5_level_0', 'T'), ('Unnamed: 6_level_0', 'Div. Finish'), ('Unnamed: 7_level_0', 'Playoffs')]]
        new_columns = []
        for col in team_table.columns:
            new_columns.append(col[-1])
        team_table.columns = new_columns
        team_table["team"] = team_abbr
        main_table = main_table.append(team_table)
    main_table = main_table.reset_index()
    return main_table
    
    
def numericalize_data(main_table):
    main_table["Playoffs"] = main_table["Playoffs"].fillna(1)
    for index, row in main_table.iterrows():
        main_table.at[index, "Div. Finish"] = numeric_dict[main_table.at[index, "Div. Finish"]] 
        main_table.at[index, "Playoffs"] = numeric_dict[main_table.at[index, "Playoffs"]]
        wins = float(main_table.at[index, "W"])
        losses = float(main_table.at[index, "L"])
        ties = float(main_table.at[index, "T"])
        numerator = wins + (0.5*ties)
        denominator = wins + losses + ties
        win_pct = numerator / denominator
        main_table.at[index, "win%"] = win_pct
    return main_table

def clean_data(main_table):
    main_table = main_table.rename(columns = {'Div. Finish':'division', 'Playoffs' : "playoffs", "Year" : "year"})
    main_table = main_table.set_index(["year", "team"])
    main_table = main_table[["win%", "division", "playoffs"]].copy()
    return main_table
    
table = get_data()
table = numericalize_data(table)
table = clean_data(table)
table.to_csv("csvs/team_record_data.csv")