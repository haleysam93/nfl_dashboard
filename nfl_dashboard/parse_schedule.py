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

def createDatabase(dirname):
    """
        This method will create the NFL database

        :param dirname: directory name where db will be stored
        :type dirname: str

        :returns: database engine connection
    """

    # Create database path
    dbPath = os.path.join(dirname, 'nfl.db')

    # If it already exists, remove the old file
    if os.path.exists(dbPath):
        os.remove(dbPath)

    # Create Engine
    engine = create_engine(
        'sqlite:///{}'.format(dbPath),
        echo=True)

    # Initialize declaritive base
    Base = declarative_base()

    class teams(Base):

        __tablename__ = 'teams'

        teams_id = Column('teams_id', Integer, primary_key=True)
        alias = Column('alias', String)
        name = Column('name', String)

    class venues(Base):

        __tablename__ =  'venues'

        venues_id = Column('venues_id', Integer, primary_key=True)
        alias = Column('alias', String)
        address = Column('address', String)
        capacity = Column('capacity', Integer)
        city = Column('city', String)
        country = Column('country', String)
        id = Column('id', String)
        name = Column('name', String)
        roof_type = Column('roof_type', String)
        state = Column('state', String)
        surface = Column('surface', String)
        zip = Column('zip', Integer)

    class games(Base):

        __tablename__ = 'games'

        games_id = Column('games_id', Integer, primary_key=True)
        datetime = Column('datetime', String)
        away = Column('away', String)
        home = Column('home', String)
        id = Column('id', String)
        week = Column('week', Integer)

    # Create schema
    Base.metadata.create_all(engine)

    return engine


def appendTables(engine, tables):
    """
        This method will append the tables to the database.

        :param engine: database connection

        :param tables: dictionary of dataframes to append to db
        :type tables: dict
    """

    for tablename, df in tables.items():
        df.to_sql(tablename, if_exists='append', con=engine, index=False)

    return


if __name__ == '__main__':


    # Get the directory where the data will be stored
    dirname = os.path.dirname(os.path.abspath(__file__))

    # Read in json file
    schedule = json.load(open('nfl_schedule.json', 'r'))

    # Parse json to get tables
    tables = parseJson(schedule)

    # Create database schema
    engine = createDatabase(dirname)

    # Append tables to database
    appendTables(engine, tables)