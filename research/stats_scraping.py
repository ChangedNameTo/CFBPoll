import pandas as pd
from pandas.io.json import json_normalize
import requests
import json

def scrape_stats():
    for year in range(2016, 2021):
        response = requests.get(
            "https://api.collegefootballdata.com/games",
            params={
                'year':year,
                'seasonType':'both'
            }
        )

        games = pd.read_json(response.text)
        games.to_csv('data/years/{}/games.csv'.format(year))

        for week in games['week'].unique():
            response = requests.get(
                "https://api.collegefootballdata.com/games/players",
                params={
                    'year':year,
                    'week':week
                }
            )
            
            with open('data/years/{}/week_{}.json'.format(year, week), 'w') as outfile:
                outfile.write(response.text)

scrape_stats()