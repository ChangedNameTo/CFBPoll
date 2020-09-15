import timeit
start = timeit.default_timer()

from pprint import pprint

import pandas as pd
import numpy as np
import cfbd

import os
import math

import datetime as dt

from Constants import WEEK, K_VALUE

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

games = pd.DataFrame()
teams = pd.DataFrame()
plays = pd.DataFrame()
stats = pd.DataFrame()
records = pd.DataFrame()

# Since we already scraped, just load in the csv dumps
# See ./research/stats_scraping.py
for year in range(2019, 2020):
    year_games = pd.read_csv('data/{}/games.csv'.format(year))
    year_teams = pd.read_csv('data/{}/teams.csv'.format(year))
    year_plays = pd.read_csv('data/{}/plays.csv'.format(year))
    year_stats = pd.read_csv('data/{}/stats.csv'.format(year))
    year_records = pd.read_csv('data/{}/records.csv'.format(year))

    games = pd.concat([games, year_games])
    teams = pd.concat([teams, year_teams])
    plays = pd.concat([plays, year_plays])
    stats = pd.concat([stats, year_stats])
    records = pd.concat([records, year_records])

# Clean the data and prep the frames
games = games[['_id','_season','_week','_season_type','_start_date','_neutral_site','_conference_game','_home_id','_home_team','_home_points','_away_id','_away_team','_away_points']]
games = pd.concat([games, pd.DataFrame(columns=['home_recent_week','home_elo','away_recent_week','away_elo','home_expected','away_expected','mov_multiplier','new_home_elo','new_away_elo','home_elo_change','away_elo_change'])])

records = records[['year', 'team','conference','division','total.games','total.wins','total.losses','conferenceGames.games','conferenceGames.wins','conferenceGames.losses']]

teams = teams[['_id','_school']]
teams = pd.concat([teams, pd.DataFrame(columns=['elo','strength_of_schedule','last_played','result','elo_change','season_record','conf_record'])])

# Joins records to teams
teams = teams.join(records)
teams = teams.drop(columns=['team'])

# Add home boolean value
games['home_won'] = games._home_points > games._away_points

# Remove the unplayed games
games['played'] = pd.to_datetime(games['_start_date'], infer_datetime_format=True).dt.tz_localize(None) < dt.datetime.now()
games.drop(games[games['played'] != True].index, inplace=True)

# Generate the FBS list, then figure out if this is an FBS matchup. Both teams must be FBS.
fbs_team_list = teams['_school'].values
games['home_fbs'] = games.apply(lambda game : (game['_home_team'] in fbs_team_list), axis=1)
games['away_fbs'] = games.apply(lambda game : (game['_away_team'] in fbs_team_list), axis=1)
games['fbs_count'] = games.apply(lambda game : (game['home_fbs'] + game['away_fbs']), axis=1)

# Begin running through games. 
def process_game(game):
    # Pull the last week played
    home_recent_week = games[((games['_home_team'] == game['_home_team']) | (games['_away_team'] == game['_home_team'])) & games['new_home_elo'].notna()]['_week']
    away_recent_week = games[((games['_home_team'] == game['_away_team']) | (games['_away_team'] == game['_away_team'])) & games['new_away_elo'].notna()]['_week']

    # Check for the beginning of the season so this doesn't error out
    game['home_recent_week'] = 0 if home_recent_week.empty else home_recent_week.max()
    game['away_recent_week'] = 0 if away_recent_week.empty else away_recent_week.max()

    # Grab the actual frame
    home_game_frame = games[((games['_home_team'] == game['_home_team']) | (games['_away_team'] == game['_home_team'])) & (games['_week'] == game['home_recent_week'])]
    away_game_frame = games[((games['_home_team'] == game['_away_team']) | (games['_away_team'] == game['_away_team'])) & (games['_week'] == game['away_recent_week'])]

    # The frame is empty at the start. If the team is fbs, seeds at 1500, else 1204
    if(home_game_frame.empty):
        if(game['home_fbs']):
            game['home_elo'] = 1500
        else:
            game['home_elo'] = 1204
    else:
        # If the last home game frame contains the home team at home, grabs that val. Else grabs away.
        if (home_game_frame['_home_team'].values[0] == game['_home_team']):
            game['home_elo'] = home_game_frame['new_home_elo'].values[0]
        else:
            game['home_elo'] = home_game_frame['new_away_elo'].values[0]
    
    if(away_game_frame.empty):
        if(game['away_fbs']):
            game['away_elo'] = 1500
        else:
            game['away_elo'] = 1204
    else:
        # If the last home game frame contains the home team at home, grabs that val. Else grabs away.
        if (away_game_frame['_home_team'].values[0] == game['_away_team']):
            game['away_elo'] = away_game_frame['new_home_elo'].values[0]
        else:
            game['away_elo'] = away_game_frame['new_away_elo'].values[0]

    # Get the expected value for this matchup. How likely is it that this team wins? Factor in the 2.5 score advantage for home 
    game['home_expected'] = (1 / (1 + 10**((game['away_elo'] - (game['home_elo'] + 25)) / 400)))
    game['away_expected'] = (1 / (1 + 10**(( game['home_elo'] - (game['away_elo'] - 25)) / 400)))

    # Get the Margin of Victory multiplier to work as a scaling factor for skill that dampens for blowouts
    # Pad by 1 to prevent 0
    log_part = math.log(abs(game['_home_points'] - game['_away_points']) + 1)

    # Scales blowouts by relative skill
    subtracted = (game['away_elo'] - game['home_elo'] if game['home_won'] else game['home_elo'] - game['away_elo'])
    multiplied_part = ( 2.2 / ((subtracted) * 0.001 + 2.2))

    # Outputs the multiplier
    game['mov_multiplier'] = log_part * multiplied_part
    
    # Calculates and outputs the new Elo's
    game['new_home_elo'] = game['home_elo'] + (K_VALUE * (int(game['home_won']) - game['home_expected']) * game['mov_multiplier'])
    game['new_away_elo'] = game['away_elo'] + (K_VALUE * (int(not game['home_won']) - game['away_expected']) * game['mov_multiplier'])

    game['home_elo_change'] = game['new_home_elo'] - game['home_elo']
    game['away_elo_change'] = game['new_away_elo'] - game['away_elo']

    # Send it back
    return game

for index,game in games.iterrows():
    games.at[index] = process_game(game)

# Drops a useless column
games = games.drop(columns=['_id'])

# Outputs all the games to a CSV
games.to_csv('processed_games.csv')

# Add's in all that other data people love
def process_team(team):
    # Grabs all of 1 teams games
    game_frame = games[((games['_home_team'] == team['_school']) | (games['_away_team'] == team['_school']))]

    # TODO: Strength of schedule

    # TODO: Add in the functionality to dump the full team spreadsheets here

    # Team hasn't yet played. Give them a 0. Since this is not in the game calculation, this will not affect future placement, so tOSU fans please don't PM me when they are ranked in the 80's
    if game_frame.empty:
        return pd.DataFrame()

    max_week = game_frame['_week'].max()

    # Grab that game, then solely pull info from it
    final_frame = game_frame[(game_frame['_week'] == max_week)]
    is_home = (final_frame['_home_team'] == team['_school']).values[0]
    result = final_frame['home_won'].values[0]
    if not is_home:
        result = not result

    text_result = 'W' if result else 'L'

    team['elo'] = round((final_frame['new_home_elo'] if is_home else final_frame['new_away_elo']).values[0],2)
    team['last_played'] = (final_frame['_away_team'] if is_home else final_frame['_home_team']).values[0]
    team['result'] = '({} - {}) {}'.format(round(final_frame['_home_points'].values[0]), round(final_frame['_away_points'].values[0]), text_result)
    team['elo_change'] = round((final_frame['home_elo_change'] if is_home else final_frame['away_elo_change']).values[0],2)
    team['season_record'] = '({} - {})'.format(team['total.wins'], team['total.losses'])
    team['conf_record'] = '({} - {})'.format(team['conferenceGames.wins'], team['total.losses'])

    return team

for index, team in teams.iterrows():
    # If the team hasn't played, excluded them from being processed and filter them later
    processed_team = process_team(team)
    if processed_team.empty:
        continue
    teams.at[index] = processed_team

teams = teams.sort_values(by=['elo'], ascending=False)
teams.index = np.arange(1, len(teams) + 1)
teams = teams.drop(columns=['year','total.games','total.wins','total.losses','conferenceGames.games','conferenceGames.wins','conferenceGames.losses'])

# Outputs all teams to a CSV
teams.to_csv('processed_teams.csv')

with open('README.md', 'w') as file:
    file.write('''# CFBPoll 4.0 by TheAlpacalypse - The Pandas Rewrite
Computerized poll to automatically rank college football teams each week

Run the program using the command:

`python3 __main__.py`

---

''')

    # Writes the table header
    file.write("|Rank|Team|Flair|Record|Elo|Last Played|Result|Change|\n")
    file.write("|---|---|---|---|---|---|---|---|\n")
    
    # Iterate over the top 25 and print them out
    for index, team in teams.iloc[:25].iterrows():
        file.write("| {} | {} | {} | {} | {} | {} | {} | {} |\n".format(index, team._school, '', team.season_record, team.elo, team.last_played, team.result, team.elo_change))

    file.write("|||||||||\n")

    # I like GT, so always print them
    gt_frame = teams[teams['_school'] == 'Georgia Tech']
    file.write("| {} | {} | {} | {} | {} | {} | {} | {} |\n".format(gt_frame.index[0], gt_frame.iloc[0]._school, '', gt_frame.iloc[0].season_record, gt_frame.iloc[0].elo, gt_frame.iloc[0].last_played, gt_frame.iloc[0].result, gt_frame.iloc[0].elo_change))
    file.write("|||||||||\n")
    
    # Lastly, always write the last place team
    file.write("| {} | {} | {} | {} | {} | {} | {} | {} |\n".format(teams.index[-1], teams.iloc[-1]._school, '', teams.iloc[-1].season_record, teams.iloc[-1].elo, teams.iloc[-1].last_played, teams.iloc[-1].result, teams.iloc[-1].elo_change))
    file.write("\n")
            
    file.write("---\n")
    file.write("\n")
    file.write("**Mean Elo:** {}\n".format(round(teams['elo'].mean(),2)))
    file.write("\n")
    file.write("**Median Elo:** {}\n".format(round(teams['elo'].median(),2)))
    file.write("\n")
    file.write("**Standard Deviation of Elo:** {}\n".format(round(teams['elo'].std(),2)))
    file.write("\n")
    file.write("[Explanation of the poll methodology here](https://www.reddit.com/user/TehAlpacalypse/comments/dwfsfi/cfb_poll_30_oops/)\n")
    file.write("\n")
    file.write("[Link to the github repository here](https://github.com/ChangedNameTo/CFBPoll)")

    stop = timeit.default_timer()

    # Fun stats for how long it took for this to generate
    file.write('')
    file.write('Ranking executed in: {}s'.format(round(stop - start,2)))