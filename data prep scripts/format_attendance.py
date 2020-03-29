# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 13:14:56 2020

@author: lemar
"""

import pandas as pd

attendance_dict = {   
        "Los Angeles Chargers" : "sdg",
        "San Francisco" : "sfo",
        "Chicago" : "chi",
        "Seattle" : "sea",
        "Minnesota" : "min",
        "New Orleans" : "nor",
        "Philadelphia" : "phi",
        "Cleveland" : "cle",
        "Denver" : "den",
        "New England" : "nwe",
        "Houston" : "htx",
        "Baltimore" : "rav",
        "Carolina" : "car",
        "Miami" : "mia",
        "Indianapolis" : "clt",
        "Kansas City" : "kan",
        "Buffalo" : "buf",
        "Green Bay" : "gnb",
        "Atlanta" : "atl",
        "NY Jets" : "nyj",
        "Detroit" : "det",
        "Arizona" : "crd",
        "Las Vegas" : "rai",
        "Tennessee" : "oti",
        "Jacksonville" : "jax",
        "Los Angeles Rams" : "ram",
        "Pittsburgh" : "pit",
        "Dallas" : "dal",
        "NY Giants" : "nyg",
        "Washington" : "was",
        "Tampa Bay" : "tam",
        "Cincinnati" : "cin"
        }

def convert_attendance_names(attendance_dict, df):
    for index, row in df.iterrows():
        df.at[index, "Team Name"] = attendance_dict[df.at[index, "Team Name"]]
    return df

def get_capacitance(attendance):
    attendance['Average'] = attendance['Average'].str.replace(',', '')
    for index, row in attendance.iterrows():
        attendance.at[index, "attend%"] = float(attendance.at[index, "Percentage"]) / 100
        attendance.at[index, "capacity"] = float(attendance.at[index, "Average"]) / float(attendance.at[index, "attend%"])
    return attendance
        
attendance = pd.read_csv("csvs/Attendance Data - Sheet1.csv")
attendance = attendance[attendance["Percentage"] != "-"]
attendance = convert_attendance_names(attendance_dict, attendance)
attendance = get_capacitance(attendance)
attendance = attendance[["Year", "Team Name", "Average", "capacity", "attend%"]].copy()
attendance.columns = ["year", "team", "attendance", "capacity", "attend%"]
attendance = attendance.set_index(["year", "team"])
attendance.to_csv("csvs/attendance_data.csv")