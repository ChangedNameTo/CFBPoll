from pprint import pprint

import pandas as pd
import numpy as np
import cfbd
import os

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

games = pd.DataFrame()
teams = pd.DataFrame()
plays = pd.DataFrame()

# This function is run once to collect the seed data for the model
for year in range(2010, 2021):
    # # Fetches all games, outputs the CSV's
    # games_result = cfbd.GamesApi().get_games(year)
    # games = pd.DataFrame.from_records([game.__dict__ for game in games_result])
    # if not os.path.exists('data/{}'.format(year)):
    #     os.makedirs('data/{}'.format(year))
    # games.to_csv('data/{}/games.csv'.format(year))

    # # Fetches all teams, outputs the CSV's
    # teams_result = cfbd.TeamsApi().get_fbs_teams(year=year)
    # teams = pd.DataFrame.from_records([team.__dict__ for team in teams_result])
    # teams.to_csv('data/{}/teams.csv'.format(year))

    # Get the highest week
    # highest_week = games['_week'].max() + 1

    # Pull all plays, concat them, then dump them into csvs
    # year_plays = pd.DataFrame()
    # for week in range(1, highest_week):
    #     print(week)
    #     plays_week_result = cfbd.PlaysApi().get_plays(year=year, week=week)
    #     plays = pd.DataFrame.from_records([play.__dict__ for play in plays_week_result])
    #     pd.concat([year_plays, plays])
    
    # year_plays.to_csv('data/{}/plays.csv'.format(year))
    year_games = pd.read_csv('data/{}/games.csv'.format(year))
    year_teams = pd.read_csv('data/{}/teams.csv'.format(year))
    year_plays = pd.read_csv('data/{}/plays.csv'.format(year))

    games = pd.concat([games, year_games])
    teams = pd.concat([teams, year_teams])
    plays = pd.concat([plays, year_plays])

teams['elo'] = 1500
print(teams.head())