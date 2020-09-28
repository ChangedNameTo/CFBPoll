import pandas as pd
import numpy as np
import os
import math
import datetime as dt
import sys
from statistics import mean

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Uncomment if this should be repulled. Else just import the dataset
games = pd.read_csv('./research/testing_data/testing_games.csv')

weekly_elos = pd.DataFrame(columns=['season','week','team','elo','is_fbs'])

weekly_elos = weekly_elos.append(games[['_season','_week','_home_team','new_home_elo','home_fbs']].rename(columns={'_season':'season','_week':'week','_home_team':'team','new_home_elo':'elo','home_fbs':'is_fbs'}))
weekly_elos = weekly_elos.append(games[['_season','_week','_away_team','new_away_elo','away_fbs']].rename(columns={'_season':'season','_week':'week','_away_team':'team','new_away_elo':'elo','away_fbs':'is_fbs'}))

# weekly_elos = pd.read_csv('./research/testing_data/aggregated_weekly_team_elos.csv')

# Culls out the FCS
weekly_elos = weekly_elos[weekly_elos['is_fbs'] == True]

# weekly_elos.to_csv('./research/testing_data/aggregated_weekly_team_elos.csv')

# Collapse the rows by team
team_names = weekly_elos.team.unique()

# Get the year rollups into a new frame
output_elos = pd.DataFrame(columns=['team'])

# Create the output array
year_corr = []

# Iterate over year
for year in range(2010, 2020):
    # Iterate over team
    for team in team_names:
        # Get the max week that your team played. THis is necessary since some teams will play more/less
        max_week = weekly_elos[((weekly_elos['team'] == team) & (weekly_elos['season'] == year))]['week'].max()

        # Some teams weren't always in the FBS. Catches errors here
        if not weekly_elos[((weekly_elos['team'] == team) & (weekly_elos['season'] == year) & (weekly_elos['week'] == max_week))]['elo'].empty:
            final_elo = weekly_elos[((weekly_elos['team'] == team) & (weekly_elos['season'] == year) & (weekly_elos['week'] == max_week))]['elo'].iloc[0]
            output_elos.loc[team, year] = final_elo
        else:
            output_elos.loc[team, year] = 1500

    # Calculates the correlation between seasons, appends it to the year_corr
    if year != 2010:
        year_corr.append(output_elos[year - 1].corr(output_elos[year]))

# Prints our output
print(mean(year_corr))

# 0.6047459547886893
# A teams next season elo is 60.47% predicatable by last seasons data. We will mean revert using this value.