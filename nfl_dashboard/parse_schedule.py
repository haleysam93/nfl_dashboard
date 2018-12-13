#! /Users/leealessandrini/anaconda3/bin/python

"""
Lee Alessandrini
Advanced Database Design Project


This module will parse and organize the nfl schedule json file into tables.
"""

import json
import pandas as pd
import os
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base


def parseJson(schedule):
    """
        This method will parse the json file and return tables.

        :param schedule: json nfl data
        :type schedule: dict

        :returns: nfl data tables
    """

    # Want to create mapping for teams and alias's, 
    teams = {'alias': [], 'name': []}
    venues = []
    games = []

    # Iterate over weeks
    weekCount = 1
    for week in schedule['weeks']:

        # Iterate over games
        for game in week['games']:

            # Get Home and Away Teams
            home = game['home']
            away = game['away']

            # Build team table and venue table
            if not home['alias'] in teams['alias']:
                # Store alias and team name
                teams['alias'].append(home['alias'])
                teams['name'].append(home['name'])
                # Store venue keys, use alias as foreign key
                venue = game['venue']
                venue['alias'] = home['alias']
                venues.append(venue)

            gameDict = {
                'home': home['alias'],
                'away': away['alias'],
                'id': game['id'],
                'datetime': game['scheduled'],
                'week': weekCount
            }

            games.append(gameDict)

    tables = {
        'venues': pd.DataFrame(venues),
        'teams': pd.DataFrame(teams),
        'games': pd.DataFrame(games)
    }

    return tables


if __name__ == '__main__':

    # Get the directory where the data will be stored
    dirname = os.path.dirname(os.path.abspath(__file__))

    # Read in json file
    schedule = json.load(open('nfl_schedule.json', 'r'))

    # Parse json to get tables
    tables = parseJson(schedule)