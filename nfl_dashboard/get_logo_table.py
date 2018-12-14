#! /Users/leealessandrini/anaconda3/bin/python
"""
This module will get the url string for each team via their alias and generate
the logo table.
"""

import pandas as pd


def getLogoTable(teamAbreviations):
    """
        This method will return a table with URL's to the official logo for
        each team.

        :param teamAbreviations: team alias column from teams database table
        :type teamAbreviations: numpy.array

        :returns: DataFrame with logo URL
    """

    # URL to official NFL logos
    URL = 'http://static.nfl.com/static/site/img/logos/500x500/{}.png'

    logoUrl = []
    for alias in teamAbreviations:
        logoUrl.append(URL.format(alias))
        
    logoTable = pd.DataFrame({
      'alias': teamAbreviations,
      'logo_url': logoUrl})

    return logoTable