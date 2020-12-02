from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

import pandas as pd

def create_model():
    games_final = pd.read_csv('data/master_games_cleaned.csv')

    games_final = games_final.fillna(0)
    games_final = games_final.drop(columns=['Unnamed: 0','game_id'])

    X_set = games_final.loc[:, games_final.columns != 'did_home_win']
    y_set = games_final.loc[:, games_final.columns == 'did_home_win']

    X_scaled = preprocessing.scale(X_set)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_set, test_size=0.3, random_state=0)

    logreg = LogisticRegression()
    logreg.fit(X_train, y_train.values.ravel())

    print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

    home_last_games = pd.read_csv('data/teams_last_game.csv')
    away_last_games = pd.read_csv('data/teams_last_game.csv')

    home_last_games = home_last_games.rename(columns={'conference':'home_conference','l3g_avg_points':'home_l3g_avg_points','l5g_avg_points':'home_l5g_avg_points','l7g_avg_points':'home_l7g_avg_points','l3g_avg_spread':'home_l3g_avg_spread','l5g_avg_spread':'home_l5g_avg_spread','l7g_avg_spread':'home_l7g_avg_spread','l3g_opp_avg_points':'home_l3g_opp_avg_points','l5g_opp_avg_points':'home_l5g_opp_avg_points','l7g_opp_avg_points':'home_l7g_opp_avg_points','l3g_opp_avg_spread':'home_l3g_opp_avg_spread','l5g_opp_avg_spread':'home_l5g_opp_avg_spread','l7g_opp_avg_spread':'home_l7g_opp_avg_spread','season_type_postseason':'season_type_postseason','season_type_regular':'season_type_regular','conference_ACC':'home_conference_ACC','conference_American Athletic':'home_conference_American Athletic','conference_Big 12':'home_conference_Big 12','conference_Big East':'home_conference_Big East','conference_Big Ten':'home_conference_Big Ten','conference_Conference USA':'home_conference_Conference USA','conference_FBS Independents':'home_conference_FBS Independents','conference_FCS':'home_conference_FCS','conference_Mid-American':'home_conference_Mid-American','conference_Mountain West':'home_conference_Mountain West','conference_Pac-12':'home_conference_Pac-12','conference_SEC':'home_conference_SEC','conference_Sun Belt':'home_conference_Sun Belt','conference_Western Athletic':'home_conference_Western Athletic','team':'home_team'})
    away_last_games = away_last_games.rename(columns={'conference':'away_conference','l3g_avg_points':'away_l3g_avg_points','l5g_avg_points':'away_l5g_avg_points','l7g_avg_points':'away_l7g_avg_points','l3g_avg_spread':'away_l3g_avg_spread','l5g_avg_spread':'away_l5g_avg_spread','l7g_avg_spread':'away_l7g_avg_spread','l3g_opp_avg_points':'away_l3g_opp_avg_points','l5g_opp_avg_points':'away_l5g_opp_avg_points','l7g_opp_avg_points':'away_l7g_opp_avg_points','l3g_opp_avg_spread':'away_l3g_opp_avg_spread','l5g_opp_avg_spread':'away_l5g_opp_avg_spread','l7g_opp_avg_spread':'away_l7g_opp_avg_spread','season_type_postseason':'season_type_postseason','season_type_regular':'season_type_regular','conference_ACC':'away_conference_ACC','conference_American Athletic':'away_conference_American Athletic','conference_Big 12':'away_conference_Big 12','conference_Big East':'away_conference_Big East','conference_Big Ten':'away_conference_Big Ten','conference_Conference USA':'away_conference_Conference USA','conference_FBS Independents':'away_conference_FBS Independents','conference_FCS':'away_conference_FCS','conference_Mid-American':'away_conference_Mid-American','conference_Mountain West':'away_conference_Mountain West','conference_Pac-12':'away_conference_Pac-12','conference_SEC':'away_conference_SEC','conference_Sun Belt':'away_conference_Sun Belt','conference_Western Athletic':'away_conference_Western Athletic','team':'away_team'})

    game_teams = pd.merge(home_last_games.assign(key=0), away_last_games.assign(key=0), on='key').drop('key', axis=1)
    game_teams['conference_game'] = game_teams['home_conference'] == game_teams['away_conference']
    game_teams['neutral_site'] = False
    game_teams['season'] = home_last_games['season'].max()
    game_teams['week'] = home_last_games['week'].max()
    game_teams['season_type_postseason'] = 0
    game_teams['season_type_regular'] = 1

    game_teams = game_teams.drop(columns=['away_conference','home_conference'], axis=1)

    game_prediction_labels = game_teams[['home_team','away_team']]
    game_prediction_set = game_teams.fillna(0)
    merge_columns = (game_prediction_set.columns.difference(X_set.columns))
    game_prediction_set = game_prediction_set.drop(columns=merge_columns, axis=1)
    
    game_set_scaled = preprocessing.scale(game_prediction_set)

    game_prediction_set['predicted_home_win'] = logreg.predict(game_set_scaled)
    game_prediction_set['predicted_home_win_percent'] = logreg.predict_proba(game_set_scaled)

    game_prediction_set = game_prediction_set.merge(game_prediction_labels, left_index=True, right_index=True)
    game_prediction_set.to_csv('data/weekly_predictions.csv', index=False)

create_model()