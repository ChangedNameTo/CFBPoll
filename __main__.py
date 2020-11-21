import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt

game_data = pd.read_csv('data/master_games.csv')

games = game_data[['away_conference','away_id','away_points','away_team','conference_game','home_conference','home_id','home_points','home_team','neutral_site','season','season_type','start_date','week']]