import pandas as pd
import numpy as np

games = pd.DataFrame()

for year in range(2019, 2020):
    year_games = pd.read_csv('data/{}/games.csv'.format(year))
    games = pd.concat([games, year_games])

games['home_spread'] = games['_home_points'] - games['_away_points']
games['home_spread'] = games['home_spread'].clip(-31, 31)

print(games['home_spread'].mean()/2)
# 3.045045045045045