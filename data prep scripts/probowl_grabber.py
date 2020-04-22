# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 12:59:41 2020

@author: lemar
"""

#import libraries, set the url
#pandas is used to easily grab tables from the page
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


team_change_dict = {
        
                "ARI" : "crd",
                "ATL" : "atl",
                "BAL" : "rav",
                "TEN" : "oti",
                "OAK" : "rai",
                "LAR" : "ram",
                "STL" : "ram",
                "LAC" : "sdg",
                "IND" : "clt",
                "HOU" : "htx"
        }

def get_per_team_count(table, team_list, first_year, last_year):
    rows = []
    for team in team_list:
        for year in range(first_year, last_year + 1):
            new_row = []
            new_row.append(team)
            new_row.append(year)
            new_table = table.loc[(table['Tm'].str.upper() == team.upper()) & (table['year'] == year)]
            new_row.append(len(new_table))
            rows.append(new_row)
    probowler_count = pd.DataFrame(rows, columns = ["team", "year", "probowler_count"])
    return probowler_count

def get_groupby_array(df, key):
    groups = df.groupby(key)
    df_array = [group for _, group in groups]
    return df_array

def fix_names(table, team_change_dict):
    for index, row in table.iterrows():
        if table.at[index, "Tm"] in team_change_dict:
            table.at[index, "Tm"] = team_change_dict[table.at[index, "Tm"]]
    return table

url_prefix = "https://www.pro-football-reference.com/years/"
url_suffix = "/probowl.htm"

main_table = pd.DataFrame()
for year in range(2006, 2020):
    new_table = pd.read_html(url_prefix + str(year) + url_suffix)[0]
    new_table["year"] = year
    main_table = main_table.append(new_table)
main_table = main_table.reset_index()
main_table = fix_names(main_table, team_change_dict)
main_table = get_per_team_count(main_table, team_list, 2006, 2019)
main_table = main_table[["year", "team", "probowler_count"]].copy()
main_table = main_table.set_index(["year", "team"])
main_table.to_csv("../csvs/probowl_data.csv")
