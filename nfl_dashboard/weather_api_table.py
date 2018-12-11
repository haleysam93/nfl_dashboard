# -*- coding: utf-8 -*-
"""
Weather Api Table

Call build_weather_table method by passing a list of zip codes and this will
return a dataframe with a three hour forecast for the next five days with
the data located in WEATHER_COLUMNS

Can make at most 60 calls to the API a minute or the account will get locked
"""

import pandas as pd
import requests
from datetime import datetime


ICON_URL = 'http://openweathermap.org/img/w/'
# Change 'weather' to 'forecast' to get 5 day every 3 hour forecast
URL = 'http://api.openweathermap.org/data/2.5/forecast?zip='
API_KEY = ',us&APPID=29ac044b94fc8a51cb5f14dc0e403d11'
ACCEPTABLE_TYPES = [int, str, float]
WEATHER_COLUMNS = ['zip_code', 'lon', 'lat', 'main', 'temp', 'pressure',
                   'humidity', 'dt', 'icon_image', 'description']

def convert_kelvin_to_fahrenheit(temp):
    """Pass a tempiture in kelvin returns the tempiture in fahrenheit"""
    return (temp - 273.15) * 9/5 + 32
    
def break_data_into_smalled_dict(data, parsing_dict):
    """Take data and break into the smallest possible dictionary"""
    while type(data) != dict or type(list(data.values())[0]) not in ACCEPTABLE_TYPES:
        if type(data) == str and data in parsing_dict and type(parsing_dict[data]) in ACCEPTABLE_TYPES:
            data = {data: parsing_dict[data]}
        elif type(data) == str and data in parsing_dict and type(parsing_dict[data]) == list:
            data = parsing_dict[data][0]
        elif type(data) == str and data in parsing_dict and type(parsing_dict[data]) == dict and len(parsing_dict[data]) != 0:
            data = parsing_dict[data]
        elif type(data) == str and data in parsing_dict and type(parsing_dict[data]) == dict and len(parsing_dict[data]) == 0:
            data = {'3h': 0.0}
        else:
            raise ValueError('Unable to break data into smallest_dict ' +
                             'data: ' + str(data))

    return data    

def append_forecast_dict(forecast_dict, smallest_dict):
    """Initialized keys in forecast_dict and appends values to keys"""
    for key in smallest_dict:
        if key in forecast_dict:
            forecast_dict[key].append(smallest_dict[key])
        else:
            forecast_dict[key] = [smallest_dict[key]]

    return forecast_dict

def build_icon_url_list(icon_list):
    """Use the list of icons to generate a list of the icon urls"""
    icon_url_list = []
    for icon in icon_list:
        icon_url_list.append(ICON_URL + icon + '.png')
    
    return icon_url_list

def append_city_df(city_df, smallest_dict):
    """Append smallest_dict data to city_df"""
    # Removing the key below because it is not always populated and
    # we don't need the data
    if '3h' in smallest_dict:
        del smallest_dict['3h']
    for key in smallest_dict:
        city_df[key] = smallest_dict[key]
        if key == 'icon':
            icon_url_list = build_icon_url_list(smallest_dict[key])
            city_df['icon_image'] = icon_url_list

    return city_df

def create_city_weather_df(zip_code):
    """Generate weather df for a city given a zip code"""
    city_df = pd.DataFrame()
    r = requests.get(URL + str(zip_code) + API_KEY)
    json_dict = r.json()
    # Initalize forecast dict to store weather data updates
    forecast_dict = {}
    # Loop through data to add each three hour update in the five day period
    for update_dict in json_dict['list']:
        for data in update_dict:
            smallest_dict = break_data_into_smalled_dict(data, update_dict)
            forecast_dict = append_forecast_dict(forecast_dict, smallest_dict)
    city_df = append_city_df(city_df, forecast_dict)
    # Loop through constant data in 'city' dictionary
    for data in json_dict['city']:
        smallest_dict = break_data_into_smalled_dict(data, json_dict['city'])
        city_df = append_city_df(city_df, smallest_dict)
    # Add remaining constants
    city_df['zip_code'] = zip_code
    city_df['cod'] = json_dict['cod']
    city_df['message'] = json_dict['message']
    city_df['cnt'] = json_dict['cnt']
        
    return city_df

def finalize_df(df):
    """Converts: tempiture to fahrenheit
                 time to datetime
    """
    df['temp'] = df['temp'].apply(convert_kelvin_to_fahrenheit)
    df['date_time'] = pd.to_datetime(df['dt'], unit='s')
    
    return df
    
def build_weather_table(zip_codes):
    """Loops through requested cities to append weather data to dataframe"""
    df = pd.DataFrame(columns=WEATHER_COLUMNS)
    for zip_code in zip_codes:
        city_df = create_city_weather_df(zip_code)
        df = pd.concat([df, city_df[WEATHER_COLUMNS]])
    df = finalize_df(df)
    
    return df