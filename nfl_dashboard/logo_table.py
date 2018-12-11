# -*- coding: utf-8 -*-
"""
from logo_table import logo_table will give user a table with all team names,
team abbreviations, and a URL to each team logo
"""

import pandas as pd

URL = 'http://static.nfl.com/static/site/img/logos/500x500/{}.png'

TEAM_NAMES = ['Cardinals',
              'Falcons',
              'Ravens',
              'Bills',
              'Panthers',
              'Bears',
              'Bengals',
              'Browns',
              'Cowboys',
              'Broncos',
              'Lions',
              'Packers',
              'Texans',
              'Colts',
              'Jaguars',
              'Chiefs',
              'Chargers',
              'Rams',
              'Dolphins',
              'Vikings',
              'Patriots',
              'Saints',
              'Giants',
              'Jets',
              'Raiders',
              'Eagles',
              'Steelers',
              'Seahawks',
              '49ers',
              'Buccaneers',
              'Titans',
              'Redskins']

TEAM_ACRONYMS = ['ARI',
                'ATL',
                'BAL',
                'BUF',
                'CAR',
                'CHI',
                'CIN',
                'CLE',
                'DAL',
                'DEN',
                'DET',
                'GB',
                'HOU',
                'IND',
                'JAX',
                'KC',
                'LAC',
                'LAR',
                'MIA',
                'MIN',
                'NE',
                'NO',
                'NYG',
                'NYJ',
                'OAK',
                'PHI',
                'PIT',
                'SEA',
                'SF',
                'TB',
                'TEN',
                'WAS']

team_logo = []
for acronym in TEAM_ACRONYMS:
    team_logo.append(URL.format(acronym))
    
logo_table = pd.DataFrame({'Team Name': TEAM_NAMES,
                           'Team Acronym': TEAM_ACRONYMS,
                           'Team Logo': team_logo})