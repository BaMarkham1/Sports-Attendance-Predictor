# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 19:55:37 2020

@author: lemar
"""

from uszipcode import SearchEngine
import json
import requests
from datetime import datetime
import sys

#zip code requested
zip_code = sys.argv[1]
#forecast requested
forecast_type = sys.argv[2]

#the following lists contain each field we want to use for each forecast type
current_key_list = ["summary", "temperature", "apparentTemperature", "precipType", "humidity", "windSpeed", "windGust", "cloudCover"]
hourly_key_list = ["summary", "temperature", "apparentTemperature", "precipType", "precipProbability", "humidity", "windSpeed", "windGust", "cloudCover"]
daily_key_list = ["summary", "temperatureHigh", "temperatureLow", "apparentTemperatureHigh", "apparentTemperatureLow", "precipType", "precipProbability", "humidity", "windSpeed", "windGust", "cloudCover"]
#this dictionary is used to refer to the lists, depending on which forecast type was requested
key_dict = {"currently" : current_key_list, "hourly" : hourly_key_list, "daily" : daily_key_list}

#gets the type of forecast requested from the zip code
def get_forecast(zip_code, forecast):
    
    #gets the location from the zip code requested
    def get_loc_from_zip(zip_code):
        #get search engine
        search = SearchEngine(simple_zipcode=True) 
        #get location info by zipcode
        zipcode = search.by_zipcode(zip_code)
        #get loc info as json
        zip_json = zipcode.to_json()
        #get loca as dictionary
        zip_dict = json.loads(zip_json)
        #get latitude and longitude from dictionary
        lati = str(zip_dict["lat"])
        longi = str(zip_dict["lng"])
        return lati, longi
    
    #get latitude and longitude from the zip code
    lati, longi = get_loc_from_zip(zip_code)
    #possible blocks returned by response if not excluded
    blocks = ["currently", "minutely", "hourly", "daily", "alerts", "flags"]
    #remove the one we actually need
    blocks.remove(forecast)
    #create comma delimited string of blocks we don't need
    blocks_to_exclude = ','.join(blocks)
    #set the api call string
    api_call = "https://api.darksky.net/forecast/cd5310da90f37ee64feb88f9ddd9837e/" + lati + "," + longi + "?exclude="  + blocks_to_exclude
    #make the api request
    response = requests.get(api_call)
    #get response as dict
    response_dict = response.json()
    #return dictionary
    return response_dict

#format the response the way we want it
def format_response(response, forecast, key_dict):
    
    #trim the response down to just the info we want
    def trim_weather_info(response_dict, key_list):
        #dictionary with only necessary info
        trimmed_dict = {}
        #add formatted time
        trimmed_dict["time"] = format_time(response_dict["time"])
        #for each key needed,
        for key in key_list:
            #if in the response, add it. If not, add -1 to indicate it's not
            if key in response_dict:
                trimmed_dict[key] = response_dict[key]
            else:
                trimmed_dict[key] = -1
        return trimmed_dict
    
    #format a unix timestamp into a human-readable format
    def format_time(timestamp):
        #get datetime object from unix timestamp
        dt = datetime.fromtimestamp(timestamp)
        #set format for time
        time_format = '%Y-%m-%d %I:%M %p'
        #return time using the datetime format
        return str(dt.strftime(time_format))
    
    #if it's the current forecast, just need to grab from one spot
    if forecast == "currently":
        #grab the info needed using trim_weather_info
        final_dict = trim_weather_info(response[forecast], key_dict[forecast])
    #if hourly or daily, iterate through the data array
    elif forecast in ["hourly","daily"]:
        final_dict = {}
        #get the main summary
        final_dict["main summary"] = response[forecast]["summary"]
        #the data entry is an array that holds each element in the array
        final_dict["data"] = []
        #for each element in the data array,
        for count,element in enumerate(response[forecast]["data"]):
            #...call trim_weather_info on each element 
            final_dict["data"].append(trim_weather_info(element, key_dict[forecast]))
    return final_dict

response = get_forecast(zip_code, forecast_type)
print(json.dumps(response, indent=4))
final_dict = format_response(response, key_dict)
print(json.dumps(final_dict, indent=4))





