import pandas as pd
import numpy as np
import cfbd
import os

import datetime as dt

from Constants import WEEK
YEAR = 2019

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

games = pd.read_csv('data/{}/games.csv'.format(YEAR))
teams = pd.read_csv('data/{}/teams.csv'.format(YEAR))
plays = pd.read_csv('data/{}/plays.csv'.format(YEAR))
stats = pd.read_csv('data/{}/stats.csv'.format(YEAR))

# Data Cleaning
games = games[['_id','_season','_week','_season_type','_start_date','_neutral_site','_conference_game','_home_id','_home_team','_home_points','_away_id','_away_team','_away_points']]
teams = teams[['_id','_school']]

# Generate the FBS list, then figure out if this is an FBS matchup. Both teams must be FBS.
fbs_team_list = teams['_school'].values
games['home_fbs'] = games.apply(lambda game : (game['_home_team'] in fbs_team_list), axis=1)
games['away_fbs'] = games.apply(lambda game : (game['_away_team'] in fbs_team_list), axis=1)
games['fbs_count'] = games.apply(lambda game : (game['home_fbs'] + game['away_fbs']), axis=1)

# Add home boolean value
games['home_won'] = games._home_points > games._away_points

# Add score differential
games['score_differential'] = abs(games._home_points - games._away_points)

# Print the value
print(games.where(games['fbs_count'] == 1)['score_differential'].mean())

# 29.69298245614035