#! /Users/leealessandrini/anaconda3/bin/python

"""
This file will function as an api test for the sportsradar api.

Source for SportRadar API python wrapper:
https://github.com/johnwmillr/SportradarAPIs

Through the free trial we have a limit to the number of queries we can perform
therefor it was more convenient to run this script seperately and save off the
results to a json file and go from there.
"""

from sportradar import NFL
import json

api_key = '4xhhfyrqycqq5h9u8wtg2m44'

# Connect to api
api = NFL.NFL(api_key, format_="json", timeout=5, sleep_time=2)
# Get the 2018 Regular season schedule
year = 2018
nfl_season = 'REG'
js = api.get_schedule(year, nfl_season).json()
# Dump the schedule to json so that you don't use up queries for the NFL api
json.dump(js, open('nfl_schedule.json', 'w'))