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
# Gotta do stats too
import statistics
# Provides the ability to shuffle the list
from random import shuffle
# Need devnull
import os

# Splitting up my file into libraries because this was tough last time
import prepoll

# Calls all of the other subordinate functions
def main(args):
    global team_list, fbs_only
    # team_list   = args[1]
    # fbs_only    = args[2]

    # Might as well just hardcode these, they don't change
    team_list   = 'util/teams.txt'
    fbs_only    = True
    week        = args[1]
    year        = args[2]

    scores        = prepoll.grab_web_page('web')
    parsed_scores = prepoll.parse_scores(scores, fbs_only, team_list)
    prepoll.output_data(parsed_scores, week, year)

    start_poll(parsed_scores, week, year)

def start_poll(parsed_scores, week, year):
    team_elo_dict = {}

    # K value manipulates how much scores are affected by results. This is super important
    k_value = 15

    # Opens the fbs team file to strip out non fbs teams
    if(fbs_only):
        fbs_teams = open(team_list, "r")
        global team_array
        team_array = []

        # Iterates to dump them all into an array
        for line in fbs_teams:
            if(len(line)>0):
                line = line.strip("\n")
                team_array.append(line)

    # This will be replaced with a carryover seed
    # Teams will retain a portion of points based on my guess of average movement
    previous_scores        = prepoll.grab_web_page('past')
    previous_parsed_scores = prepoll.parse_scores(previous_scores, fbs_only, team_list)
    team_elo_dict          = previous_season(previous_parsed_scores)

    # shuffle(parsed_scores)
    for score in parsed_scores:
        # Checks that the teams involved are actually in the dict
        # Defaults to 400 points below the default 1500 points. This equates to an average team
        # supposed to beat a cupcake by at least 20 points
        if score[1] in team_elo_dict.keys():
            rating_home = team_elo_dict[score[1]]
            null_home   = False
        else:
            rating_home = 1100
            null_home   = True

        if score[3] in team_elo_dict.keys():
            rating_away = team_elo_dict[score[3]]
            null_away   = False
        else:
            rating_away = 1100
            null_away   = True

        # Expected odds
        expected_home = 1 / ( 1 + 10**( ( rating_away - rating_home ) / 400 ) )
        expected_away = 1 / ( 1 + 10**( ( rating_home - rating_away ) / 400 ) )

        # Updating rating
        # First see the winner
        # Also includes a MoV multiplier
        if(int(score[2]) > int(score[4])):
            home_score = 1
            away_score = 0
            mom_multiplier = math.log(abs(int(score[2]) - int(score[4]))) * (2.2 / ((rating_home - rating_away)*0.001 + 2.2))
        else:
            home_score = 0
            away_score = 1
            mom_multiplier = math.log(abs(int(score[2]) - int(score[4]))) * (2.2 / ((rating_away - rating_home)*0.001 + 2.2))

        # Apply the function for updating ratings
        new_rating_home = rating_home + k_value * (home_score - expected_home) * mom_multiplier
        new_rating_away = rating_away + k_value * (away_score - expected_away) * mom_multiplier

        # Check that the new ratings for winners is actually higher
        if(home_score == 1):
            new_rating_home = max(new_rating_home, rating_home)

        if(away_score == 1):
            new_rating_away = max(new_rating_away, rating_away)

        # Sets the new ratings for each team in the map
        if not null_home:
            team_elo_dict[score[1]] = new_rating_home

        if not null_away:
            team_elo_dict[score[3]] = new_rating_away

    # Sorts the dictionary, popping out each max point team and appending them to the list
    final_ranking  = []
    temp_point_map = copy.deepcopy(team_elo_dict)

    for x in range(0,len(team_elo_dict)):
        highest_team = max(team_elo_dict.items(), key=operator.itemgetter(1))[0]
        final_ranking.append(highest_team)
        del team_elo_dict[highest_team]

    math_stats = math_stats_calculations(temp_point_map)
    extra_stats = extra_stats_parsing(parsed_scores)
    last_week = previous_change(week, year, final_ranking)
    markdown_output(temp_point_map, final_ranking, extra_stats, math_stats, last_week)
    final_rankings_graph(temp_point_map, final_ranking, extra_stats, math_stats, last_week, week, year)
    season_output(week, year)

# Calculates the elo for the previous season to seed this upcoming season
def previous_season(parsed_scores):
    team_elo_dict = {}

    # K value manipulates how much scores are affected by results. This is super important
    k_value = 15

    # Opens the fbs team file to strip out non fbs teams
    if(fbs_only):
        fbs_teams = open(team_list, "r")
        global team_array
        team_array = []

        # Iterates to dump them all into an array
        for line in fbs_teams:
            if(len(line)>0):
                line = line.strip("\n")
                team_array.append(line)

    for team in team_array:
        team_elo_dict[team] = 1500

    # shuffle(parsed_scores)
    for score in parsed_scores:
        # Checks that the teams involved are actually in the dict
        # Defaults to 400 points below the default 1500 points. This equates to an average team
        # supposed to beat a cupcake by at least 20 points
        if score[1] in team_elo_dict.keys():
            rating_home = team_elo_dict[score[1]]
            null_home   = False
        else:
            rating_home = 1100
            null_home   = True

        if score[3] in team_elo_dict.keys():
            rating_away = team_elo_dict[score[3]]
            null_away   = False
        else:
            rating_away = 1100
            null_away   = True

        # Expected odds
        expected_home = 1 / ( 1 + 10**( ( rating_away - rating_home ) / 400 ) )
        expected_away = 1 / ( 1 + 10**( ( rating_home - rating_away ) / 400 ) )

        # Updating rating
        # First see the winner
        # Also includes a MoV multiplier
        if(int(score[2]) > int(score[4])):
            home_score = 1
            away_score = 0
            mom_multiplier = math.log(abs(int(score[2]) - int(score[4]))) * (2.2 / ((rating_home - rating_away)*0.001 + 2.2))
        else:
            home_score = 0
            away_score = 1
            mom_multiplier = math.log(abs(int(score[2]) - int(score[4]))) * (2.2 / ((rating_away - rating_home)*0.001 + 2.2))

        # Apply the function for updating ratings
        new_rating_home = rating_home + k_value * (home_score - expected_home) * mom_multiplier
        new_rating_away = rating_away + k_value * (away_score - expected_away) * mom_multiplier

        # Check that the new ratings for winners is actually higher
        if(home_score == 1):
            new_rating_home = max(new_rating_home, rating_home)

        if(away_score == 1):
            new_rating_away = max(new_rating_away, rating_away)

        # Sets the new ratings for each team in the map
        if not null_home:
            team_elo_dict[score[1]] = new_rating_home

        if not null_away:
            team_elo_dict[score[3]] = new_rating_away

    # Sorts the dictionary, popping out each max point team and appending them to the list
    final_ranking  = []
    temp_point_map = copy.deepcopy(team_elo_dict)

    for x in range(0,len(team_elo_dict)):
        highest_team = max(team_elo_dict.items(), key=operator.itemgetter(1))[0]
        final_ranking.append(highest_team)
        del team_elo_dict[highest_team]

    math_stats = math_stats_calculations(temp_point_map)
    extra_stats = extra_stats_parsing(parsed_scores)
    # Fix this next season
    last_season_graph(temp_point_map, final_ranking, extra_stats, math_stats, 'Final', str(2017))

    for team in team_array:
        temp_point_map[team] = (temp_point_map[team] - 1500) * (-0.66) + temp_point_map[team]
    return temp_point_map

# Creates a markdown table that can be posting into the reddit comments section
def markdown_output(point_map,final_ranking,extra_stats,math_stats, last_week):
    # Opens the file
    with open("ranking.txt", "w") as file:
        # Writes the table header
        file.write("|Rank|Team|Flair|Record|SoS^^1|SoS Rank|ELO|Change|\n")
        file.write("|---|---|---|---|---|---|---|---|\n")

        # Terminates the ranking after 25
        x = 1

        # Pulls sos for everyone
        output      = calculate_sos(final_ranking,extra_stats)
        sos_map     = output[0]
        sos_ranking = output[1]

        # Creates the flair map for everyone
        flair_map = generate_flair_map()

        for team in final_ranking:
            # Calculates some things here to pretty up the string itself
            # Looks weird cause python is weird and does weird things
            sos      = str(sos_map[team])
            sos_rank = sos_ranking[team]
            sos_rank = str(sos_rank)
            record   = str(extra_stats[1][team][0]) + "-" + str(extra_stats[1][team][1])
            change   = str(last_week[team])

            # Writes to the file
            file.write("|" + str(x) + "|" + team + "|" + flair_map[team] + "|" + record + "|" + sos + "|" + sos_rank + "|" + str(round(point_map[team], 2)) + "|" + change + "|\n")
            x = x + 1

            # Terminates after 25
            if x == 26:
                break

        # Outputs GT's data cause I like them
        file.write("||||||||\n")
        team     = 'Georgia Tech'
        rank     = final_ranking.index(team) + 1
        sos      = str(sos_map[team])
        sos_rank = sos_ranking[team]
        sos_rank = str(sos_rank)
        record   = str(extra_stats[1][team][0]) + "-" + str(extra_stats[1][team][1])
        change   = str(last_week[team])

        # Writes to the file
        file.write("|" + str(rank) + "|" + team + "|" + flair_map[team] + "|" + record + "|" + sos + "|" + sos_rank + "|" + str(round(point_map[team], 2)) + "|" + change + "|\n")

        # Outputs the lowest team too just for fun
        file.write("||||||||\n")
        team     = final_ranking[len(final_ranking) - 1]
        rank     = final_ranking.index(team) + 1
        sos      = str(sos_map[team])
        sos_rank = sos_ranking[team]
        sos_rank = str(sos_rank)
        record   = str(extra_stats[1][team][0]) + "-" + str(extra_stats[1][team][1])
        change   = str(last_week[team])

        # Writes to the file
        file.write("|" + str(rank) + "|" + team + "|" + flair_map[team] + "|" + record + "|" + sos + "|" + sos_rank + "|" + str(round(point_map[team], 2)) + "|" + change + "|\n")

        file.write("\n")

        # Writes out the easiest and hardest SoS
        for key, value in sos_ranking.items():
            if value == 1:
                easiest = key
            if value == 130:
                hardest = key

        file.write("---\n")
        file.write("\n")
        file.write("**Mean Points:** " + math_stats[0] + "\n")
        file.write("\n")
        file.write("**Median Points:** " + math_stats[1] + "\n")
        file.write("\n")
        file.write("**Standard Deviation of Points:** " + math_stats[2] + "\n")
        file.write("\n")
        file.write("**Variance:** " + math_stats[3] + "\n")
        file.write("\n")
        file.write("---\n")
        file.write("\n")
        file.write("**Hardest SoS:** " + flair_map[easiest] + " " + easiest + "\n")
        file.write("\n")
        file.write("**Easiest SoS:** " + flair_map[hardest] + " " + hardest + "\n")
        file.write("\n")
        file.write("---\n")
        file.write("\n")
        file.write("1: Lower means harder SoS\n")
        file.write("\n")
        file.write("[Explanation of the poll methodology here](https://www.reddit.com/user/TehAlpacalypse/comments/9csiv4/cfb_poll_20_the_elo_update/)\n")
        file.write("\n")
        file.write("[Link to the github repo here](https://github.com/ChangedNameTo/CFBPoll)")

# Iterates through all of the scores, generates a map of opponents so SoS can be done later
# Also tracks the records so that total game count is known
def extra_stats_parsing(parsed_scores):
    opponents_map = {}
    records_map = {}

    # Creates the arrays so no errors are thrown
    for team in team_array:
        opponents_map[team] = []
        records_map[team] = [0,0]

    # Iterates through all scores, if the team isn't in the team array does nothing
    for score in parsed_scores:
        # Pulls opponents data
        if score[1] in opponents_map.keys():
            opponents_map[score[1]].append(score[3])
        if score[3] in opponents_map.keys():
            opponents_map[score[3]].append(score[1])

        # Pulls record data, records_map[team] = [W, L]
        if int(score[2]) > int(score[4]):
            if score[1] in records_map.keys():
                records_map[score[1]][0] = records_map[score[1]][0] + 1
            if score[3] in records_map.keys():
                records_map[score[3]][1] = records_map[score[3]][1] + 1

        # Away Wins
        if int(score[2]) < int(score[4]):
            if score[1] in records_map.keys():
                records_map[score[1]][1] = records_map[score[1]][1] + 1
            if score[3] in records_map.keys():
                records_map[score[3]][0] = records_map[score[3]][0] + 1

    # Returns the opponents map
    return (opponents_map, records_map)

# Uses the final rankings to calculate strength of schedule for a team using
# the average rank of their opponents. Lower is better.
def calculate_sos(final_rankings, extra_stats):
    sos_map = {}

    for team in team_array:
        # Averages out final ranks of opponents. If the opponent is non fbs,
        # assumes they would have finished 130
        sos_total  = 0
        team_total = extra_stats[1][team][0] + extra_stats[1][team][1] + 1

        # Fetchs the list of opponents
        opponents_list = extra_stats[0][team]

        # Grabs their final rankings
        for opponent in opponents_list:
            if opponent in final_rankings:
                sos_total = sos_total + final_rankings.index(opponent)
            else:
                sos_total = sos_total + len(final_rankings)

        # Averages them out and records them. Rounds to three for appearances
        sos_average   = sos_total / team_total
        sos_map[team] = round(sos_average, 3)

    # Variables for calculating the ranking of a teams SOS
    sos_ranking = {}
    sos_map_copy = copy.deepcopy(sos_map)

    # Ranks the teams from easiest to hardest SOS. Smaller number = harder SoS
    for x in range(1,len(sos_map_copy)+1):
        lowest_team = min(sos_map_copy.items(), key=operator.itemgetter(1))[0]
        sos_ranking[lowest_team] = x
        del sos_map_copy[lowest_team]
    return (sos_map,sos_ranking)

# Sets up the flair map that will be searchable for the markdown
def generate_flair_map():
    flair_map = {}

    # Reads in the flair map
    with open('util/flair_list.csv') as flair_csv:
        csvReader = csv.reader(flair_csv)
        for row in csvReader:
            # Formats the flair strings then adds them to the map
            flair_map[row[0]] = "[" + row[0] + "]" + "(#f/" + row[1] + ")"

    return flair_map

def last_season_graph(point_map, final_ranking, extra_stats, math_stats, week, year):
    with open(str(year) + '/week' + week + '.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(('Rank','Team','Record','SoS','SoS Rank','ELO'))

        # Terminates the ranking after 25
        x = 1

        # Pulls sos for everyone
        output      = calculate_sos(final_ranking,extra_stats)
        sos_map     = output[0]
        sos_ranking = output[1]

        # Creates the flair map for everyone
        flair_map = generate_flair_map()

        for team in final_ranking:
            # Calculates some things here to pretty up the string itself
            # Looks weird cause python is weird and does weird things
            sos      = str(sos_map[team])
            sos_rank = sos_ranking[team]
            sos_rank = str(sos_rank)
            record   = str(extra_stats[1][team][0]) + "-" + str(extra_stats[1][team][1])

            # Writes to the csv
            writer.writerow([x,team,record,sos,sos_rank,str(round(point_map[team], 2))])
            x = x + 1

def final_rankings_graph(point_map, final_ranking, extra_stats, math_stats, last_week, week, year):
    with open(str(year) + '/week' + week + '.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(('Rank','Team','Record','SoS','SoS Rank','ELO','Change'))

        # Terminates the ranking after 25
        x = 1

        # Pulls sos for everyone
        output      = calculate_sos(final_ranking,extra_stats)
        sos_map     = output[0]
        sos_ranking = output[1]

        # Creates the flair map for everyone
        flair_map = generate_flair_map()

        for team in final_ranking:
            # Calculates some things here to pretty up the string itself
            # Looks weird cause python is weird and does weird things
            sos      = str(sos_map[team])
            sos_rank = sos_ranking[team]
            sos_rank = str(sos_rank)
            record   = str(extra_stats[1][team][0]) + "-" + str(extra_stats[1][team][1])
            change   = str(last_week[team])

            # Writes to the csv
            writer.writerow([x,team,record,sos,sos_rank,str(round(point_map[team], 2)),change])
            x = x + 1

# Calculates them math class stats
def math_stats_calculations(point_map):
    point_array = []
    for team in team_array:
        point_array.append(point_map[team])

    # Calculates mean
    mean_val   = str(round(statistics.mean(point_array), 2))
    # Calculates median
    median_val = str(round(statistics.median(point_array), 2))
    # Calculates standard deviation
    stdev_val  = str(round(statistics.stdev(point_array), 2))
    # Calculates variance
    var_val    = str(round(statistics.variance(point_array), 2))

    return (mean_val,median_val,stdev_val,var_val)

# Calculates the difference in ranks from week to week
def previous_change(week, year, final_ranking):
    f             = open(str(year) + "/week" + str(int(week) - 1) + ".csv", 'r')
    previous_week = csv.reader(f)

    # Tracks the change for each team from week to week
    change_map = {}

    x = 1
    for team in final_ranking:
        for row in previous_week:
            if team == row[1]:
                change_map[team] = int(row[0]) - x
                continue
        f.seek(0)
        x = x + 1

    return change_map

# Season ranking evolution output for fun
def season_output(week, year):
    # Opens the file
    with open("season_evolution.txt", "w") as file:
        # Writes the table header
        file.write("|Week\Rank|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|\n")
        file.write("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")

        # Creates the flair map for everyone
        flair_map = generate_flair_map()

        for x in range(1,int(week) + 1):
            # Create the week string
            week_string = "|" + str(x) + "|"

            # Iterates over each of the weekly csvs
            f        = open(str(year) + "/week" + str(x) + ".csv", 'r')
            week_csv = csv.reader(f)
            next(week_csv, None)

            # Leave loop at 25
            breakout = 1
            for team in week_csv:
                week_string = week_string + flair_map[team[1]] + "|"
                breakout = breakout + 1
                if breakout > 25:
                    break

            # Writes to the file
            file.write(week_string + "\n")

# Calls my function
if __name__ == '__main__':
    import sys
    main(sys.argv)
