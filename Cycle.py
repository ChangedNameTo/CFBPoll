import pandas as pd
import numpy as np
import math

# We need to run this fresh every time, as adjustments should propogate to avoid years falling out of sync
class Cycle:
    def __init__(self,options,year):
        self.iter_year = year
        self.k_value = options['k_value']
        self.mean_reversion = options['mean_reversion']
        self.fcs_elo = options['fcs_elo']
        self.start_year = options['start_year']
        self.hfa = options['hfa']
        self.end_year = options['end_year']
        self.week = options['week']

    def run(self):
        # Since we already scraped, just load in the csv dumps
        # See ./research/stats_scraping.py
        games = pd.read_csv('data/{}/games.csv'.format(self.iter_year))
        teams = pd.read_csv('data/{}/teams.csv'.format(self.iter_year))
        plays = pd.read_csv('data/{}/plays.csv'.format(self.iter_year))
        stats = pd.read_csv('data/{}/stats.csv'.format(self.iter_year))
        records = pd.read_csv('data/{}/records.csv'.format(self.iter_year))
        flair = pd.read_csv('data/flair_list.csv')

        if self.iter_year != self.start_year:
            previous_teams = pd.read_csv('data/{}/processed_teams.csv'.format(self.iter_year - 1))

        # Clean the data and prep the frames
        games = games[['_id','_season','_week','_season_type','_start_date','_neutral_site','_conference_game','_home_team','_home_points','_away_team','_away_points']]
        games = pd.concat([games, pd.DataFrame(columns=['home_recent_week','home_elo','away_recent_week','away_elo','home_expected','away_expected','mov_multiplier','new_home_elo','new_away_elo','home_elo_change','away_elo_change','predicted_home_win','predicted_away_win','correct_prediction'])])

        records = records[['year', 'team','conference','division','total.games','total.wins','total.losses','conferenceGames.games','conferenceGames.wins','conferenceGames.losses']]

        teams = teams[['_id','_school']]
        teams = pd.concat([teams, pd.DataFrame(columns=['elo','_year','strength_of_schedule','last_played','result','elo_change','season_record','conf_record'])])

        # Joins records to teams
        teams = teams.set_index('_school',drop=False)
        records = records.set_index('team',drop=False)
        teams = teams.join(records)
        
        # Joins flair to teams
        flair = flair.set_index('school',drop=False)
        teams = teams.join(flair)
        
        # Drops the column joins
        teams = teams.drop(columns=['team'])
        teams = teams.drop(columns=['school'])

        # Adds the year
        teams['_year'] = self.iter_year

        # Resets the index to a number 
        teams.index = np.arange(1, len(teams) + 1)

        # Add home boolean value
        games['home_won'] = games._home_points > games._away_points
        games['away_won'] = ~games['home_won']

        # Remove the unplayed games
        games['played'] = games['_home_points'].notna()
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

            # The frame is empty at the start. 
            if(home_game_frame.empty):
                if(game['home_fbs']):
                    # How are we getting our seed value? Is it the default of 1500, or the mean reverted value?
                    if self.iter_year == self.start_year:
                        game['home_elo'] = 1500
                    else:
                        seed_elo = previous_teams[(previous_teams['_school'] == game['_home_team'])]
                        if not seed_elo['elo'].empty:
                            game['home_elo'] = ((seed_elo['elo'].values[0] - 1500) * self.mean_reversion) + 1500
                            # game['home_elo'] = 1500
                        else:
                            game['home_elo'] = 1500
                else:
                    game['home_elo'] = self.fcs_elo
            else:
                # If the last home game frame contains the home team at home, grabs that val. Else grabs away.
                if (home_game_frame['_home_team'].values[0] == game['_home_team']):
                    game['home_elo'] = home_game_frame['new_home_elo'].values[0]
                else:
                    game['home_elo'] = home_game_frame['new_away_elo'].values[0]
            
            if(away_game_frame.empty):
                if(game['away_fbs']):
                    # How are we getting our seed value? Is it the default of 1500, or the mean reverted value?
                    if self.iter_year == self.start_year:
                        game['away_elo'] = 1500
                    else:
                        seed_elo = previous_teams[(previous_teams['_school'] == game['_away_team'])]
                        if not seed_elo['elo'].empty:
                            # game['away_elo'] = 1500
                            game['away_elo'] = ((seed_elo['elo'].values[0] - 1500) * self.mean_reversion) + 1500
                        else:
                            game['away_elo'] = 1500
                else:
                    game['away_elo'] = self.start_year
            else:
                # If the last home game frame contains the home team at home, grabs that val. Else grabs away.
                if (away_game_frame['_home_team'].values[0] == game['_away_team']):
                    game['away_elo'] = away_game_frame['new_home_elo'].values[0]
                else:
                    game['away_elo'] = away_game_frame['new_away_elo'].values[0]

            # Get the expected value for this matchup. How likely is it that this team wins? Factor in the 3.04 score advantage for home
            # That we calculated in ./research/get_hfa_value.py, round it cause variance
            game['home_expected'] = (1 / (1 + 10**((game['away_elo'] - (game['home_elo'] + self.hfa)) / 400)))
            game['away_expected'] = (1 / (1 + 10**(( game['home_elo'] - (game['away_elo'] - self.hfa)) / 400)))

            # Get the Margin of Victory multiplier to work as a scaling factor for skill that dampens for blowouts
            # Pad by 1 to prevent 0
            log_part = math.log(abs(game['_home_points'] - game['_away_points']) + 1)

            # Scales blowouts by relative skill
            subtracted = (game['away_elo'] - game['home_elo'] if game['home_won'] else game['home_elo'] - game['away_elo'])
            multiplied_part = ( 2.2 / ((subtracted) * 0.001 + 2.2))

            # Outputs the multiplier
            game['mov_multiplier'] = log_part * multiplied_part
            
            # Calculates and outputs the new Elo's
            game['new_home_elo'] = game['home_elo'] + (self.k_value * (int(game['home_won']) - game['home_expected']) * game['mov_multiplier'])
            game['new_away_elo'] = game['away_elo'] + (self.k_value * (int(not game['home_won']) - game['away_expected']) * game['mov_multiplier'])

            # Records the change from the previous weeks output
            game['home_elo_change'] = game['new_home_elo'] - game['home_elo']
            game['away_elo_change'] = game['new_away_elo'] - game['away_elo']

            # Checks which team we expected to win. Did they win? Helps develop model feedback
            game['predicted_home_win'] = game['home_expected'] > game['away_expected']
            game['predicted_away_win'] = game['home_expected'] < game['away_expected']
            game['correct_prediction'] = ((game['home_won'] and game['predicted_home_win']) or (game['away_won'] and game['predicted_away_win']))

            # Send it back
            return game

        for index,game in games.iterrows():
            games.at[index] = process_game(game)

        # Drops a useless column
        games = games.drop(columns=['_id'])

        # Outputs all the games to a CSV
        games.to_csv('./data/{}/processed_games.csv'.format(self.iter_year))

        # Add's in all that other data people love
        def process_team(team):
            # Grabs all of 1 teams games
            game_frame = games.loc[((games['_home_team'] == team['_school']) | (games['_away_team'] == team['_school']))]

            # Calculates trength of schedule as a function of the opponent elo at the time you played them
            game_frame.loc[game_frame['_home_team'] != team['_school'], 'opponent_elo'] = game_frame['home_elo']
            game_frame.loc[game_frame['_away_team'] != team['_school'], 'opponent_elo'] = game_frame['away_elo']
            team['strength_of_schedule'] = round(game_frame.opponent_elo.mean(), 2)

            # TODO: Add in the functionality to dump the full team spreadsheets here

            # Team hasn't yet played. Give them a 0. Since this is not in the game calculation, this will not affect future placement, so tOSU fans please don't PM me when they are ranked in the 80's
            if game_frame.empty:
                return pd.DataFrame()

            max_week = game_frame['_week'].max()

            # Grab that game, then solely pull info from it
            final_frame = game_frame[(game_frame['_week'] == max_week)]

            # Is this team home
            is_home = (final_frame['_home_team'] == team['_school']).values[0]

            # Win or Lose?
            result = final_frame['home_won'].values[0]
            if not is_home:
                result = not result

            # Convert bool to W/L
            text_result = 'W' if result else 'L'

            # Gets the current elo
            team['elo'] = round((final_frame['new_home_elo'] if is_home else final_frame['new_away_elo']).values[0],2)

            # Grabs the name of the last team played
            team['last_played'] = (final_frame['_away_team'] if is_home else final_frame['_home_team']).values[0]

            # Creates the Results Column
            if is_home:
                team['result'] = '(**{}** - {}) {}'.format(round(final_frame['_home_points'].values[0]), round(final_frame['_away_points'].values[0]), text_result)
            else:
                team['result'] = '({} - **{}**) {}'.format(round(final_frame['_home_points'].values[0]), round(final_frame['_away_points'].values[0]), text_result)

            team['elo_change'] = round((final_frame['home_elo_change'] if is_home else final_frame['away_elo_change']).values[0],2)
            team['season_record'] = '({} - {})'.format(round(team['total.wins']), round(team['total.losses']))
            team['conf_record'] = '({} - {})'.format(round(team['conferenceGames.wins']), round(team['total.losses']))

            return team

        for index, team in teams.iterrows():
            # If the team hasn't played, excluded them from being processed and filter them later
            processed_team = process_team(team)
            if processed_team.empty:
                continue
            teams.at[index] = processed_team

        teams['played'] = teams['total.games'].notna()
        teams.drop(teams[teams['played'] != True].index, inplace=True)

        # Sorts the teams by Elo
        teams = teams.sort_values(by=['elo'], ascending=False)

        # Re-indexes so that I can use the index column for rank
        teams.index = np.arange(1, len(teams) + 1)

        # Drops excess columns that were used for derived values
        teams = teams.drop(columns=['_id','year','total.games','total.wins','total.losses','conferenceGames.games','conferenceGames.wins','conferenceGames.losses'])

        # Outputs all teams to a CSV
        teams.to_csv('./data/{}/processed_teams.csv'.format(self.iter_year))

        # Strength of Schedule Rankings
        sos = teams.sort_values(by=['strength_of_schedule'], ascending=False)
        sos.index = np.arange(1,len(sos) + 1)

        # Season prediction quality outputs
        number_correct_season = len(games[(games['correct_prediction'] == True)])
        number_of_games = len(games)
        season_percent_correct = round(((number_correct_season / number_of_games) * 100), 2)

        if(self.iter_year == self.end_year):
            with open('README.md', 'w') as file:
                file.write('# CFBPoll 4.0 by TheAlpacalypse - The Pandas Rewrite\n')
                file.write('\n')
                file.write('Computerized poll to automatically rank college football teams each week\n')
                file.write('First install the dependencies using the command:\n')
                file.write('\n')
                file.write('`pip install -r requirements.txt`\n')
                file.write('\n')
                file.write('Then run the program using the command:\n')
                file.write('\n')
                file.write('`python3 __main__.py`\n')
                file.write('\n')
                file.write('Use `Constants.py` to tweak the values I use to generate the ranking. I have tried to avoid leaving any raw values in this main program to let users experiment.\n')
                file.write('\n')
                file.write('---\n')

                # Writes the table header
                file.write("|Rank|Team|Flair|Record|Elo|Last Played|Result|Change|\n")
                file.write("|---|---|---|---|---|---|---|---|\n")
                
                # Iterate over the top 25 and print them out
                for index, team in teams.iloc[:25].iterrows():
                    file.write("| {} | {} | [](#f/{}) | {} | {} | {} | {} | {} |\n".format(index, team._school, team.flair, team.season_record, team.elo, team.last_played, team.result, team.elo_change))

                file.write("|||||||||\n")

                # I like GT, so always print them
                gt_frame = teams[teams['_school'] == 'Georgia Tech']
                file.write("| {} | {} | [](#f/{}) | {} | {} | {} | {} | {} |\n".format(gt_frame.index[0], gt_frame.iloc[0]._school, gt_frame.iloc[0].flair, gt_frame.iloc[0].season_record, gt_frame.iloc[0].elo, gt_frame.iloc[0].last_played, gt_frame.iloc[0].result, gt_frame.iloc[0].elo_change))
                file.write("|||||||||\n")
                
                # Lastly, always write the last place team
                file.write("| {} | {} | [](#f/{}) | {} | {} | {} | {} | {} |\n".format(teams.index[-1], teams.iloc[-1]._school, teams.iloc[-1].flair, teams.iloc[-1].season_record, teams.iloc[-1].elo, teams.iloc[-1].last_played, teams.iloc[-1].result, teams.iloc[-1].elo_change))
                file.write("\n")
                        
                file.write("---\n")
                file.write("\n")
                file.write("**Mean Elo:** {}\n".format(round(teams['elo'].mean(),2)))
                file.write("\n")
                file.write("**Median Elo:** {}\n".format(round(teams['elo'].median(),2)))
                file.write("\n")
                file.write("**Standard Deviation of Elo:** {}\n".format(round(teams['elo'].std(),2)))
                file.write("\n")

                # Strength of Schedule Outputs 
                file.write("**Easiest Strength of Schedule:** {}\n".format(sos.iloc[-1]._school))
                file.write("\n")
                file.write("**Hardest Strength of Schedule:** {}\n".format(sos.iloc[0]._school))
                file.write("\n")

                # Season prediction quality outputs
                number_correct_season = len(games[(games['correct_prediction'] == True)])
                number_of_games = len(games)
                season_percent_correct = round(((number_correct_season / number_of_games) * 100), 2)

                file.write("**Predictions Quality (Season):** {}% Correct\n".format(season_percent_correct))

                # Weekly quality outputs
                # Now for the current week
                file.write("\n")
                number_correct_curr_week =  len(games[(games['correct_prediction'] == True) & (games['_week'] == self.week)])
                number_of_games_curr_week = len(games[games['_week'] == self.week])
                curr_week_percent_correct = round(((number_correct_curr_week / number_of_games_curr_week) * 100), 2)
                
                # And then the last week
                number_correct_last_week =  len(games[(games['correct_prediction'] == True) & (games['_week'] == self.week - 1)])
                number_of_games_last_week = len(games[games['_week'] == self.week - 1])
                last_week_percent_correct = round(((number_correct_last_week / number_of_games_last_week) * 100), 2)

                file.write("**Predictions Quality (Week):** {}% Correct (Last Week: {}%)\n".format(curr_week_percent_correct, last_week_percent_correct))
                file.write("\n")
                file.write("[Explanation of the poll methodology here](https://www.reddit.com/user/TehAlpacalypse/comments/dwfsfi/cfb_poll_30_oops/)\n")
                file.write("\n")
                file.write("[Link to the github repository here](https://github.com/ChangedNameTo/CFBPoll)\n")
    
        return [self.iter_year,season_percent_correct]

    # elif TESTING:
    #     testing_games = pd.concat([testing_games, games])
    #     testing_plays = pd.concat([testing_plays, plays])
    #     testing_teams = pd.concat([testing_teams, teams])
    #     testing_games = pd.concat([testing_games, games])

    # if TESTING:
    #     testing_games.to_csv('./research/testing_data/testing_games.csv')
    #     testing_plays.to_csv('./research/testing_data/testing_plays.csv')
    #     testing_teams.to_csv('./research/testing_data/testing_teams.csv')
    #     testing_stats.to_csv('./research/testing_data/testing_stats.csv')