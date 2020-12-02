import pandas as pd

def generate_outputs():
    df = pd.read_csv('data/weekly_predictions.csv')
    predictions = df[['home_team','away_team','predicted_home_win']]

    team_dict = {}

    counter = 0
    for team in predictions['home_team'].unique():
        team_games = predictions[predictions['home_team'] == team]
        wins = team_games[team_games['predicted_home_win'] == True].count()['predicted_home_win']
        losses = team_games[team_games['predicted_home_win'] == False].count()['predicted_home_win']
        team_dict[counter] = {'team':team,'wins':wins,'losses':losses, 'total':(wins+losses)}
        counter += 1

    team_rollups = pd.DataFrame(data=team_dict).transpose()
    team_rollups['win_percent'] = team_rollups['wins'] / team_rollups['total']

    team_rollups = team_rollups[['team','win_percent']]

    print(team_rollups)
generate_outputs()