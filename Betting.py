from Constants import ODDS_URL, BASE_URL

import requests, time, csv
from datetime import datetime

r = requests.get(url = ODDS_URL)
odds_data = r.json()

games = odds_data[0]['events']

with open('cfb_odds.csv', 'w') as odds_csv:
    writer = csv.writer(odds_csv, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(('Game ID','Game Time','Home','H Spread','H Odds','Away','A Spread','A Odds','URL'))

    for game in games:
        game_id = game['id']
        game_url = BASE_URL + game['link']
        game_time = datetime.fromtimestamp((game['startTime']/1000.0))

        competitors = game['competitors']
        for competitor in competitors:
            if competitor['home'] == True:
                home = competitor['name']
            if competitor['home'] == False:
                away = competitor['name']

        odds = game['displayGroups'][0]['markets']

        for odds_type in odds:
            if odds_type['description'] == 'Point Spread':
                outcomes = odds_type['outcomes']
                for outcome in outcomes:
                    team_name = outcome['description']
                    if team_name == home:
                        home_spread = outcome['price']['handicap']
                        home_odds = outcome['price']['american']
                    if team_name == away:
                        away_spread = outcome['price']['handicap']
                        away_odds = outcome['price']['american']

        writer.writerow((game_id,game_time,home,home_spread,home_odds,away,away_spread,away_odds,game_url))

class Betting(object):
    pass