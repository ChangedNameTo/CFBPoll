import pandas as pd

pd.set_option('display.max_columns', None)

def data_cleaning():
    game_data = pd.read_csv('data/master_games.csv')

    games = game_data[['game_id','away_conference','away_points','away_team','conference_game','home_conference','home_points','home_team','neutral_site','season','season_type','week']]

    games['home_conference'] = games['home_conference'].fillna('FCS')
    games['away_conference'] = games['away_conference'].fillna('FCS')

    games['did_home_win'] = games['home_points'] > games['away_points']

    games['fbs_matchup'] = games.apply(lambda game : ((game['away_conference'] != 'FCS') and (game['home_conference'] != 'FCS')), axis=1)

    games['total_points'] = games['away_points'] + games['home_points']

    games['home_spread'] = games['home_points'] - games['away_points']
    games['away_spread'] = ~games['home_spread']


    games['home_l3g_avg_points'] = games.apply(lambda game: games[(games['home_team'] == game['home_team'])].iloc[-4:-1]['home_points'].mean(), axis=1)
    games['home_l5g_avg_points'] = games.apply(lambda game: games[(games['home_team'] == game['home_team'])].iloc[-6:-1]['home_points'].mean(), axis=1)
    games['home_l7g_avg_points'] = games.apply(lambda game: games[(games['home_team'] == game['home_team'])].iloc[-8:-1]['home_points'].mean(), axis=1)

    games['away_l3g_avg_points'] = games.apply(lambda game: games[(games['away_team'] == game['away_team'])].iloc[-4:-1]['away_points'].mean(), axis=1)
    games['away_l5g_avg_points'] = games.apply(lambda game: games[(games['away_team'] == game['away_team'])].iloc[-6:-1]['away_points'].mean(), axis=1)
    games['away_l7g_avg_points'] = games.apply(lambda game: games[(games['away_team'] == game['away_team'])].iloc[-8:-1]['away_points'].mean(), axis=1)


    games['home_l3g_avg_spread'] = games.apply(lambda game: games[(games['home_team'] == game['home_team'])].iloc[-4:-1]['home_spread'].mean(), axis=1)
    games['home_l5g_avg_spread'] = games.apply(lambda game: games[(games['home_team'] == game['home_team'])].iloc[-6:-1]['home_spread'].mean(), axis=1)
    games['home_l7g_avg_spread'] = games.apply(lambda game: games[(games['home_team'] == game['home_team'])].iloc[-8:-1]['home_spread'].mean(), axis=1)

    games['away_l3g_avg_spread'] = games.apply(lambda game: games[(games['away_team'] == game['away_team'])].iloc[-4:-1]['away_spread'].mean(), axis=1)
    games['away_l5g_avg_spread'] = games.apply(lambda game: games[(games['away_team'] == game['away_team'])].iloc[-6:-1]['away_spread'].mean(), axis=1)
    games['away_l7g_avg_spread'] = games.apply(lambda game: games[(games['away_team'] == game['away_team'])].iloc[-8:-1]['away_spread'].mean(), axis=1)


    games['home_l3g_opp_avg_points'] = games.apply(lambda game: games[(games['home_team'] == game['home_team'])].iloc[-4:-1]['away_points'].mean(), axis=1)
    games['home_l5g_opp_avg_points'] = games.apply(lambda game: games[(games['home_team'] == game['home_team'])].iloc[-6:-1]['away_points'].mean(), axis=1)
    games['home_l7g_opp_avg_points'] = games.apply(lambda game: games[(games['home_team'] == game['home_team'])].iloc[-8:-1]['away_points'].mean(), axis=1)

    games['away_l3g_opp_avg_points'] = games.apply(lambda game: games[(games['away_team'] == game['away_team'])].iloc[-4:-1]['home_points'].mean(), axis=1)
    games['away_l5g_opp_avg_points'] = games.apply(lambda game: games[(games['away_team'] == game['away_team'])].iloc[-6:-1]['home_points'].mean(), axis=1)
    games['away_l7g_opp_avg_points'] = games.apply(lambda game: games[(games['away_team'] == game['away_team'])].iloc[-8:-1]['home_points'].mean(), axis=1)


    games['home_l3g_opp_avg_spread'] = games.apply(lambda game: games[(games['home_team'] == game['home_team'])].iloc[-4:-1]['away_spread'].mean(), axis=1)
    games['home_l5g_opp_avg_spread'] = games.apply(lambda game: games[(games['home_team'] == game['home_team'])].iloc[-6:-1]['away_spread'].mean(), axis=1)
    games['home_l7g_opp_avg_spread'] = games.apply(lambda game: games[(games['home_team'] == game['home_team'])].iloc[-8:-1]['away_spread'].mean(), axis=1)

    games['away_l3g_opp_avg_spread'] = games.apply(lambda game: games[(games['away_team'] == game['away_team'])].iloc[-4:-1]['home_spread'].mean(), axis=1)
    games['away_l5g_opp_avg_spread'] = games.apply(lambda game: games[(games['away_team'] == game['away_team'])].iloc[-6:-1]['home_spread'].mean(), axis=1)
    games['away_l7g_opp_avg_spread'] = games.apply(lambda game: games[(games['away_team'] == game['away_team'])].iloc[-8:-1]['home_spread'].mean(), axis=1)


    team_names = games[['game_id','home_team','away_team','home_conference','away_conference']]
    games = games[['game_id','did_home_win','conference_game','neutral_site','season','season_type','away_conference','home_conference','week','away_l3g_avg_points','away_l5g_avg_points','away_l7g_avg_points','home_l3g_avg_points','home_l5g_avg_points','home_l7g_avg_points','home_l3g_avg_spread','home_l5g_avg_spread','home_l7g_avg_spread','away_l3g_avg_spread','away_l5g_avg_spread','away_l7g_avg_spread','home_l3g_opp_avg_points','home_l5g_opp_avg_points','home_l7g_opp_avg_points','away_l3g_opp_avg_points','away_l5g_opp_avg_points','away_l7g_opp_avg_points','home_l3g_opp_avg_spread','home_l5g_opp_avg_spread','home_l7g_opp_avg_spread','away_l3g_opp_avg_spread','away_l5g_opp_avg_spread','away_l7g_opp_avg_spread']]


    cat_vars=['season_type','away_conference','home_conference']
    for var in cat_vars:
        cat_list='var' + '_' + var
        cat_list = pd.get_dummies(games[var], prefix=var)
        data1 = games.join(cat_list)
        games = data1

    cat_vars = ['season_type','away_conference','home_conference']
    games_vars = games.columns.values.tolist()
    to_keep = [i for i in games_vars if i not in cat_vars]

    games_final = games[to_keep]

    team_names.to_csv('data/master_team_names_cleaned.csv', index=False)
    games_final.to_csv('data/master_games_cleaned.csv', index=False)