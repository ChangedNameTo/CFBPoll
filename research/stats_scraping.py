import cfbd
import pandas as pd
import requests

def scrape_stats():
    for year in range(2010, 2021):
        conferences = [
            'ACC',
            'B12',
            'B1G',
            'SEC',
            'PAC',

            'CUSA',
            'MAC',
            'MWC',
            'AAC',
            'SBC',

            'Ind'
        ]

        for conference in conferences:
            response = requests.get(
                "https://api.collegefootballdata.com/games",
                params={
                    'year':year,
                    'seasonType':'both',
                    'conference':conference 
                }
            )

            conference_games = pd.read_json(response.text)
            conference_games.to_csv('data/{}/{}_games.csv'.format(year, conference))
        
        response = requests.get(
            "https://api.collegefootballdata.com/games",
            params={
                'year':year,
                'seasonType':'both',
                'conference':conference 
            }
        )

        games = pd.read_json(response.text)
        games.to_csv('data/{}/games.csv'.format(year))

scrape_stats()