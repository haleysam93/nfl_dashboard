#! /Users/leealessandrini/anaconda3/bin/python

"""
Lee Alessandrini
Advanced Database Design Project


This module will create the sqlite database
"""

# Import packages
import os
import json
import pandas as pd
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Import local modules
import parse_schedule
import get_news


def main():
    """
        This method will execute various models to collect data from online
        API's and insert those tables into a sqlite database.
    """

    # Get the directory where the data will be stored
    dirname = os.path.dirname(os.path.abspath(__file__))
    # Get NFL schedule json as dict
    schedule = getSchedule()
    # Parse json into DataFrames
    tables = parse_schedule.parseJson(schedule)
    # Get news table
    tables['news'] = getNews(tables['teams'])
    # Create database schema
    engine = createDatabase(dirname)
    # Append tables to database
    appendTables(engine, tables)

    return


def getSchedule():
    """
        This method will get the NFL schedule from the saved json file.

        :returns: schedule dict
    """

    # Get the directory where the data will be stored
    dirname = os.path.dirname(os.path.abspath(__file__))

    # Read in json file
    schedule = json.load(open('nfl_schedule.json', 'r'))

    return schedule


def getNews(teams):
    """
        This method will get the news table using the get_news module.

        :param teams: teams table
        :type teams: pandas.DataFrame

        :returns: news table
    """
    # Get array of team names
    teamNames = teams['name'].values
    # Get news DataFrame
    news = get_news.get_news(teamNames)
    # Merge to get team abbreviation
    news = pd.merge(teams,
                    news.rename(columns={'search_key': 'name'}),
                    on='name',
                    how='right')
    # Drop name column
    news.drop(labels=['name'], axis=1, inplace=True)

    return news


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

    class news(Base):

        __tablename__ = 'news'

        news_id = Column('news_id', Integer, primary_key=True)
        alias = Column('alias', String)
        date = Column('date', String)
        description = Column('description', String)
        source = Column('source', String)
        title = Column('title', String)
        url = Column('url', String)

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

    # Run main method
    main()