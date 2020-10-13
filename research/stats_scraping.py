import cfbd
import pandas as pd
import os
import glob
import json
import requests

from pandas.io.json import json_normalize

def scrape_stats(end_week):
    for year in range(2020, 2021):
        # Fetches all games, outputs the CSV's
        games_result = cfbd.GamesApi().get_games(year, season_type='both')
        games = pd.DataFrame.from_records([game.__dict__ for game in games_result])
        if not os.path.exists('data/{}'.format(year)):
            os.makedirs('data/{}'.format(year))
        games.to_csv('data/{}/games.csv'.format(year))

        # # Fetches all teams, outputs the CSV's
        teams_result = cfbd.TeamsApi().get_fbs_teams(year=year)
        teams = pd.DataFrame.from_records([team.__dict__ for team in teams_result])
        teams.to_csv('data/{}/teams.csv'.format(year))

        # # Pull all plays, concat them, then dump them into csvs
        year_plays = pd.DataFrame()
        for week in range(1, end_week + 1):
            plays_week_result = cfbd.PlaysApi().get_plays(year=year, week=week)
            plays = pd.DataFrame.from_records([play.__dict__ for play in plays_week_result])
            year_plays = pd.concat([year_plays, plays])

        year_plays.to_csv('data/{}/plays.csv'.format(year))

        # # Pull all advanced stats, concat them, then dump them into csvs
        year_stats = pd.DataFrame()
        for week in range(1, end_week + 1):
            stats_week_result = cfbd.StatsApi().get_team_season_stats(year=year, start_week=week, end_week=week+1)
            stats = pd.DataFrame.from_records([stat.__dict__ for stat in stats_week_result])
            year_stats = pd.concat([year_stats, stats])

        year_stats.to_csv('data/{}/stats.csv'.format(year))

        response = requests.get('https://api.collegefootballdata.com/records?year={}'.format(year))
        json_records = response.json()
        records = pd.json_normalize(json_records)

        records.to_csv('data/{}/records.csv'.format(year))