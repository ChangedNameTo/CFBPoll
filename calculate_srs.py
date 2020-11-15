import pandas as pd
import numpy as np
import cfbd

def calculate_srs(file_path):
    data = pd.read_csv(file_path)

    data = data[
        (data['home_points'] == data['home_points']) # filtering out future games
        & (data['away_points'] == data['away_points'])
        & (pd.notna(data['home_conference'])) # games with a non-FBS home team
        & (pd.notna(data['away_conference'])) # games with a non-FBS away team
    ]

    data['home_spread'] = np.where(data['neutral_site'] == True, data['home_points'] - data['away_points'], (data['home_points'] - data['away_points'] - 2.5))
    data['away_spread'] = -data['home_spread']


    teams = pd.concat([
        data[['home_team', 'home_spread', 'away_team']].rename(columns={'home_team': 'team', 'home_spread': 'spread', 'away_team': 'opponent'}),
        data[['away_team', 'away_spread', 'home_team']].rename(columns={'away_team': 'team', 'away_spread': 'spread', 'home_team': 'opponent'})
    ])

    teams.head()

    teams['spread'] = np.where(teams['spread'] > 28, 28, teams['spread']) # cap the upper bound scoring margin at +28 points
    teams['spread'] = np.where(teams['spread'] < -28, -28, teams['spread']) # cap the lower bound scoring margin at -28 points
    teams.head()

    spreads = teams.groupby('team').spread.mean()


    # create empty arrays
    terms = []
    solutions = []

    for team in spreads.keys():
        row = []
        # get a list of team opponents
        opps = list(teams[teams['team'] == team]['opponent'])
        
        for opp in spreads.keys():
            if opp == team:
                # coefficient for the team should be 1
                row.append(1)
            elif opp in opps:
                # coefficient for opponents should be 1 over the number of opponents
                row.append(-1.0/len(opps))
            else:
                # teams not faced get a coefficient of 0
                row.append(0)
                
        terms.append(row)
        
        # average game spread on the other side of the equation
        solutions.append(spreads[team])

    solutions = np.linalg.solve(np.array(terms), np.array(solutions))

    ratings = list(zip( spreads.keys(), solutions ))
    srs = pd.DataFrame(ratings, columns=['team', 'rating'])

    rankings = srs.sort_values('rating', ascending=False).reset_index()[['team', 'rating']]

    return rankings.loc[:]