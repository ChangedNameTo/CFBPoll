from Constants import ODDS_URL, BASE_URL

import requests, time, csv, re
from datetime import datetime

r = requests.get(url = ODDS_URL)
odds_data = r.json()

games = odds_data[0]['events']

team_names = []

def extract_name(team_name):
    return re.findall('^([\w\s&-]*?)\s?[\(#\d\)]*\s*?$',team_name)[0]

with open('cfb_odds.csv', 'w') as odds_csv:
    writer = csv.writer(odds_csv, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(('Game ID','Game Time','Home','Home Spread','Home Odds','Away','Away Spread','Away Odds','URL'))

    for game in games:
        game_id = game['id']
        game_url = BASE_URL + game['link']
        game_time = datetime.fromtimestamp((game['startTime']/1000.0))

        competitors = game['competitors']
        for competitor in competitors:
            if competitor['home'] == True:
                home = extract_name(competitor['name'])
                if home not in team_names:
                    team_names.append(home)
            if competitor['home'] == False:
                away = extract_name(competitor['name'])
                if away not in team_names:
                    team_names.append(away)

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

with open('bovada_names.txt', 'w') as file:
    for name in team_names:
        file.write(name+'\n')

class Betting(object):
    pass