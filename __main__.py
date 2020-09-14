from pprint import pprint

import pandas as pd
import numpy as np
import cfbd
import os

import datetime as dt

from Constants import WEEK

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

# Seed ELO and Week
teams['elo'] = 1500
teams['week'] = 0

# Clean the data
games = games[['_id','_season','_week','_season_type','_start_date','_neutral_site','_conference_game','_home_id','_home_team','_home_points','_away_id','_away_team','_away_points']]
teams = teams[['_id','_school']]

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

def process_game(game):
    print(game)
    home_team = game['_home_team']
    away_team = game['_away_team']

    # We want the highest week played
    game['home_elo'] = teams.iloc[teams[teams['_school'] == home_team]['week'].argmax()]['elo']
    game['away_elo'] = teams.iloc[teams[teams['_school'] == away_team]['week'].argmax()]['elo']

    # Get the expected value for this matchup. How likely is it that this team wins? 
    # game[]
    
    game['fbs_matchup'] = (home_team in fbs_teams_list or away_team in fbs_teams_list)

games.apply(process_game, axis=1)

print(games.head())
# print(games.shape)