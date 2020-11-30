import ast
import pandas as pd
from pandas.io.json import json_normalize

def only_dict(d):
    '''
    Convert json string representation of dictionary to a python dict
    '''
    return ast.literal_eval(d)

def list_of_dicts(ld):
    '''
    Create a mapping of the tuples formed after 
    converting json strings of list to a python list   
    '''
    return dict([(list(d.values())[1], list(d.values())[0]) for d in ast.literal_eval(ld)])

# A = json_normalize(df['columnA'].apply(only_dict).tolist()).add_prefix('columnA.')
# B = json_normalize(df['columnB'].apply(list_of_dicts).tolist()).add_prefix('columnB.pos.') 

for year in range(2010,2021):
    games = pd.read_csv('data/years/{}/games.csv'.format(year))

    for week in games['week'].unique():
        with open('data/years/{}/week_{}.json'.format(year, week)) as stats_file:
            week_stats = pd.read_json(stats_file)

            teams = json_normalize(week_stats['teams'].apply(list_of_dicts).tolist()).add_prefix('teams.pos.')
        break
    
    break