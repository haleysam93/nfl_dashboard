#! /Users/leealessandrini/anaconda3/bin/python

"""
This file will function as an api test for the sportsradar api
"""

api_key = '4xhhfyrqycqq5h9u8wtg2m44'

from sportradar import NFL
import json

# Connect to api
api = NFL.NFL(api_key, format_="json", timeout=5, sleep_time=2)

"""
game_id = "b1dbf64f-822a-49b7-9bf3-070f5d6da827"

bs = api.get_game_boxscore(game_id)

print(bs) 
"""

year = 2018
nfl_season = 'REG'
js = api.get_schedule(year, nfl_season).json()

json.dump(js, open('nfl_schedule.json', 'w'))