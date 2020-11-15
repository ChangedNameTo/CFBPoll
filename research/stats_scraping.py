import cfbd
import pandas as pd
import requests

def scrape_stats():
    for year in range(2010, 2021):
        response = requests.get(
            "https://api.collegefootballdata.com/games",
            params={
                'year':year,
                'seasonType':'both'
            }
        )

        games = pd.read_json(response.text)
        games.to_csv('data/{}/games.csv'.format(year))

scrape_stats()