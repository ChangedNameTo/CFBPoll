from pprint import pprint

import pandas as pd
import numpy as np
import cfbd

import os
import math

import datetime as dt

from Constants import WEEK, K_VALUE

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

games = pd.DataFrame()
teams = pd.DataFrame()
plays = pd.DataFrame()
stats = pd.DataFrame()

# This function is run once to collect the seed data for the model
for year in range(2020, 2021):
# for year in range(2019, 2020):
    # Fetches all games, outputs the CSV's
    # games_result = cfbd.GamesApi().get_games(year)
    # games = pd.DataFrame.from_records([game.__dict__ for game in games_result])
    # if not os.path.exists('data/{}'.format(year)):
    #     os.makedirs('data/{}'.format(year))
    # games.to_csv('data/{}/games.csv'.format(year))

    # # Fetches all teams, outputs the CSV's
    # teams_result = cfbd.TeamsApi().get_fbs_teams(year=year)
    # teams = pd.DataFrame.from_records([team.__dict__ for team in teams_result])
    # teams.to_csv('data/{}/teams.csv'.format(year))

    # Pull all plays, concat them, then dump them into csvs
    # year_plays = pd.DataFrame()
    # for week in range(1, WEEK + 1):
    #     plays_week_result = cfbd.PlaysApi().get_plays(year=year, week=week)
    #     plays = pd.DataFrame.from_records([play.__dict__ for play in plays_week_result])
    #     year_plays = pd.concat([year_plays, plays])

    # year_plays.to_csv('data/{}/plays.csv'.format(year))

    # Pull all advanced stats, concat them, then dump them into csvs
    # year_stats = pd.DataFrame()
    # for week in range(1, highest_week):
    #     stats_week_result = cfbd.StatsApi().get_team_season_stats(year=year, start_week=week, end_week=week+1)
    #     stats = pd.DataFrame.from_records([stat.__dict__ for stat in stats_week_result])
    #     year_stats = pd.concat([year_stats, stats])

    # year_stats.to_csv('data/{}/stats.csv'.format(year))

    # Since we already scraped, just load in the csv dumps
    year_games = pd.read_csv('data/{}/games.csv'.format(year))
    year_teams = pd.read_csv('data/{}/teams.csv'.format(year))
    year_plays = pd.read_csv('data/{}/plays.csv'.format(year))
    year_stats = pd.read_csv('data/{}/stats.csv'.format(year))

    games = pd.concat([games, year_games])
    teams = pd.concat([teams, year_teams])
    plays = pd.concat([plays, year_plays])
    stats = pd.concat([stats, year_stats])

# Clean the data and prep the frames
games = games[['_id','_season','_week','_season_type','_start_date','_neutral_site','_conference_game','_home_id','_home_team','_home_points','_away_id','_away_team','_away_points']]
teams = teams[['_id','_school']]

# Seed ELO and Week
teams['elo'] = 1500
teams['week'] = 0

# Add home boolean value
games['home_won'] = games._home_points > games._away_points

# Remove the unplayed games
games['played'] = pd.to_datetime(games['_start_date'], infer_datetime_format=True).dt.tz_localize(None) < dt.datetime.now()
games.drop(games[games['played'] != True].index, inplace=True)

# Generate the FBS list, then figure out if this is an FBS matchup. Both teams must be FBS.
fbs_team_list = teams['_school'].values
games['home_fbs'] = games.apply(lambda game : (game['_home_team'] in fbs_team_list), axis=1)
games['away_fbs'] = games.apply(lambda game : (game['_away_team'] in fbs_team_list), axis=1)
games['fbs_count'] = games.apply(lambda game : (game['home_fbs'] + game['away_fbs']), axis=1)

# Begin running through games. 

# Pull Home Elo
games['home_recent_week'] = games.apply(lambda game: (teams[teams['_school'] == game['_home_team']]['week'].argmax() if game['home_fbs'] else None), axis=1) 
games['home_elo'] = games.apply(lambda game: (teams.loc[(teams['_school'] == game['_home_team']) & (teams['week'] == game['home_recent_week'])]['elo'].values[0] if game['home_fbs'] else 1204), axis=1)

# Pull Away Elo
games['away_recent_week'] = games.apply(lambda game: (teams[teams['_school'] == game['_away_team']]['week'].argmax() if game['away_fbs'] else None), axis=1) 
games['away_elo'] = games.apply(lambda game: (teams.loc[(teams['_school'] == game['_away_team']) & (teams['week'] == game['away_recent_week'])]['elo'].values[0] if game['away_fbs'] else 1204), axis=1)

# Get the expected value for this matchup. How likely is it that this team wins? Factor in the 2.5 score advantage for home 
games['home_expected'] = games.apply(lambda game: (1 / (1 + 10**((game['away_elo'] - (game['home_elo'] + 25)) / 400))), axis=1)
games['away_expected'] = games.apply(lambda game: (1 / (1 + 10**(( game['home_elo'] - (game['away_elo'] - 25)) / 400))), axis=1)

def mov_multiplier(game):
    # Get the Margin of Victory multiplier to work as a scaling factor for skill that dampens for blowouts
    # Pad by 1 to prevent 0
    log_part = math.log(abs(game['_home_points'] - game['_away_points']) + 1)

    # Scales blowouts by relative skill
    subtracted = (game['away_elo'] - game['home_elo'] if game['home_won'] else game['home_elo'] - game['away_elo'])
    multiplied_part = ( 2.2 / ((subtracted) * 0.001 + 2.2))

    # Outputs the multiplier
    return log_part * multiplied_part

games['mov_multiplier'] = games.apply(mov_multiplier, axis=1)

# Calculates and outputs the new Elo's
games['new_home_elo'] = games.apply(lambda game: game['home_elo'] + (K_VALUE * (int(game['home_won']) - game['home_expected']) * game['mov_multiplier']), axis=1)
games['new_away_elo'] = games.apply(lambda game: game['away_elo'] + (K_VALUE * (int(not game['home_won']) - game['away_expected']) * game['mov_multiplier']), axis=1)

games.to_csv('test.csv')

# Puts them into the team table


# Spits out a ranking

# Spits out csvs

print(games.head())