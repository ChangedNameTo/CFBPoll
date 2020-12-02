from data_cleaning import data_cleaning
from team_stats_combined import last_games
from model import create_model
from outputs import generate_outputs

data_cleaning()
last_games()
create_model()
generate_outputs()