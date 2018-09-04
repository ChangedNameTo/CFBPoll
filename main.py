# College football poll designed and maintained by /u/TehAlpacalypse

# Grabs the web pages
import urllib.request
# Dumps all of this data to a csv
import csv
# Allows us to shuffle the array every cycle
import random
# Allows the sorting of the array
import operator
# Allows map copying to make sense
import copy
# Threading will make the entire thing run faster, which was a problem V1.
import threading
# Gotta do math
import math

# Splitting up my file into libraries because this was tough last time
import prepoll

# Calls all of the other subordinate functions
def main(args):
    global team_list, fbs_only
    output_file = args[1]
    team_list   = args[2]
    fbs_only    = args[3]

    scores        = prepoll.grab_web_page()
    parsed_scores = prepoll.parse_scores(scores)

    prepoll.output_data(parsed_scores, output_file)

    start_poll(parsed_scores)

def start_poll(parsed_scores):
    team_elo_dict = {}

    # K value manipulates how much scores are affected by results. This is super important
    k_value = 20

    for team in team_list:
        # This will be replaced with a carryover seed
        # Teams will retain a portion of points based on my guess of average movement
        # To run multiple sims at once, use multiprocessing:
        # https://stackoverflow.com/questions/7207309/python-how-can-i-run-python-functions-in-parallel
        team_elo_dict[team] = 1500

    for score in parsed_scores:
        # Checks that the teams involved are actually in the dict
        # Defaults to 400 points below the default 1500 points. This equates to an average team
        # supposed to beat a cupcake by at least 20 points
        if score[1] in team_elo_dict.keys():
            rating_home = team_elo_dict[score[1]]
            null_home   = False
        else:
            null_home   = True
            rating_home = 1100

        if score[3] in team_elo_dict.keys():
            rating_away = team_elo_dict[score[3]]
            null_away   = False
        else:
            null_away   = True
            rating_away = 1100

        # Expected odds
        expected_home = 1 / ( 1 + 10**( ( rating_away - rating_home ) / 400 ) )
        expected_away = 1 / ( 1 + 10**( ( rating_home - rating_away ) / 400 ) )

        # Updating rating
        # First see the winner
        # Also includes a MoV multiplier
        if(int(score[2]) > int(score[4])):
            home_score = 1
            away_score = 0
            mom_multiplier = math.log(abs(score[2] - score[4])) * (2.2 / ((rating_home - rating_away)*0.001 + 2.2))
        else:
            home_score = 0
            away_score = 1
            mom_multiplier = math.log(abs(score[2] - score[4])) * (2.2 / ((rating_away - rating_home)*0.001 + 2.2))

        # Apply the function for updating ratings
        new_rating_home = rating_home + k_value(home_score - expected_home)
        new_rating_away = rating_away + k_value(away_score - expected_away)

        # Check that the new ratings for winners is actually higher
        if(home_score == 1):
            new_rating_home = max(new_rating_home, rating_home)

        if(away_score == 1):
            new_rating_away = max(new_rating_away, rating_away)

        # Sets the new ratings for each team in the map
        if not null_home:
            team_elo_dict[score[1]] = new_rating_home

        if not null_away:
            team_elo_dict[score[1]] = new_rating_home

    print(team_elo_dict)
