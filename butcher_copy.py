# College football poll designed and maintained by /u/TehAlpacalypse

# Web Parser
from bs4 import BeautifulSoup
# Grabs the web pages
import urllib.request
# Regexes for stripping and such
import re
# Dumps all of this data to a csv
import csv
# Allows us to shuffle the array every cycle
import random
# Allows the sorting of the array
import operator
# Allows map copying to make sense
import copy
# Lets me get stats for the whole list which are cool and make people
# think I know what I'm doing
import statistics

# Calls all of the other subordinate functions
def main(args):
    global team_list, fbs_only

    output_file = args[1]
    team_list   = args[2]
    fbs_only    = args[3]

    scores        = grab_web_page()
    parsed_scores = parse_scores(scores)

    output_data(parsed_scores, output_file)

    start_poll(parsed_scores)















# Sets up all of the poll variables
def start_poll(parsed_scores):
    # Sets up the master map that will hold all of the points over poll cycles
    team_point_map = {}

    for team in team_array:
        team_point_map[team] = 0

    y = 1000
    for x in range(0,y):
        print("Cycle " + str(x) + " of " + str(y))
        cycle_map = poll_cycle(parsed_scores)

        # Adds this cycle's points to the main map
        for team in team_array:
            team_point_map[team] = cycle_map[team] + team_point_map[team]

    # Sorts the dictionary, popping out each max point team and appending them to the list
    final_ranking  = []
    temp_point_map = copy.deepcopy(team_point_map)

    for x in range(0,len(team_point_map)):
        highest_team = max(team_point_map.items(), key=operator.itemgetter(1))[0]
        final_ranking.append(highest_team)
        del team_point_map[highest_team]

    final_rankings_graph(temp_point_map)
    math_stats = math_stats_calculations(temp_point_map)
    extra_stats = extra_stats_parsing(parsed_scores)
    markdown_output(temp_point_map, final_ranking, extra_stats, math_stats)

def poll_cycle(parsed_scores):
    # Shuffles the team array for a random pass
    random.shuffle(team_array)
    # Sets up the team point dict to track points for this cycle
    cycle_map = {}

    # Tracking map for the debugging
    tracking_map = {}

    # Seeds the initial team array point values
    x = 0
    for team in team_array:
        cycle_map[team]    = len(team_array) - x
        tracking_map[team] = []
        x                  = x + 1

    # Sets the value of the team_point_map to start it off
    team_point_map = copy.deepcopy(cycle_map)

    # Iterate through the scores, moving teams around in the array and adding up points
    # Poll positions only need to update when dates change
    # random.shuffle(parsed_scores)
    for score in parsed_scores:

        # Updates the point map with the initial values for positions so this is bias agnostic
        team_point_map = {}
        temp_cycle_map = copy.deepcopy(cycle_map)
        temp_array = []
        for x in range(0,len(temp_cycle_map)):
            highest_team = max(temp_cycle_map.items(), key=operator.itemgetter(1))[0]
            team_point_map[highest_team] = len(temp_cycle_map) - x
            temp_array.append(highest_team)
            tracking_map[highest_team].append(temp_array.index(highest_team))
            del temp_cycle_map[highest_team]

        # Stores scores so they add without being affected by change
        # if the team is not in the list they aren't fbs, therefore they are a cupcake.
        # Beating cupcakes awards no points

        # Home Wins
        if int(score[2]) > int(score[4]):
            if score[1] in cycle_map.keys():
                try:
                    cycle_map[score[1]] = cycle_map[score[1]] + (len(temp_array) - temp_array.index(score[3]))
                except ValueError as inst:
                    pass
            if score[3] in cycle_map.keys():
                try:
                    cycle_map[score[3]] = cycle_map[score[3]] - temp_array.index(score[1])
                except ValueError as inst:
                    cycle_map[score[3]] = cycle_map[score[3]] - len(temp_array)

        # Away Wins
        if int(score[2]) < int(score[4]):
            if score[3] in cycle_map.keys():
                try:
                    cycle_map[score[3]] = cycle_map[score[3]] + (len(temp_array) - temp_array.index(score[1]))
                except ValueError as inst:
                    pass
            if score[1] in cycle_map.keys():
                try:
                    cycle_map[score[1]] = cycle_map[score[1]] - temp_array.index(score[3])
                except ValueError as inst:
                    cycle_map[score[1]] = cycle_map[score[1]] - len(temp_array)
                    pass

    # After all scores have been iterated through, returns the map to the master so it can update scores
    # debug_poll(tracking_map)
    return cycle_map

# Outputs the team movement over a cycle to see how the movement is happening
# def debug_poll(tracking_map):
#     with open('debug.csv', 'w') as csvfile:
#         writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
#         writer.writerow(('Date','Ranks'))
#         for key, value in tracking_map.items():
#             value.insert(0, key)
#             writer.writerow(value)

# Creates a markdown table that can be posting into the reddit comments section
def markdown_output(point_map,final_ranking,extra_stats,math_stats):
    # Opens the file
    with open("ranking.txt", "w") as file:
        # Writes the table header
        file.write("|Rank|Team|Flair|Record|SoS^^1|SoS Rank|Points|\n")
        file.write("|---|---|---|---|---|---|---|\n")

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

            # Writes to the file
            file.write("|" + str(x) + "|" + team + "|" + flair_map[team] + "|" + record + "|" + sos + "|" + sos_rank + "|" + str(point_map[team]) + "|\n")
            x = x + 1

            # Terminates after 25
            if x == 26:
                break

        # Outputs GT's data cause I like them
        file.write("||||||||\n")
        team = 'Georgia Tech'
        rank     = final_ranking.index(team) + 1
        sos      = str(sos_map[team])
        sos_rank = sos_ranking[team]
        sos_rank = str(sos_rank)
        record   = str(extra_stats[1][team][0]) + "-" + str(extra_stats[1][team][1])

        # Writes to the file
        file.write("|" + str(rank) + "|" + team + "|" + flair_map[team] + "|" + record + "|" + sos + "|" + sos_rank + "|" + str(point_map[team]) + "|\n")

        file.write("\n")

        # Writes out the easiest and hardest SoS
        for key, value in sos_ranking.items():
            if value == 1:
                easiest = key
            if value == 129:
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
        file.write("1: Lower means harder SoS")
        file.write("\n")
        file.write("[Explanation of the poll methodology here](https://www.reddit.com/user/TehAlpacalypse/comments/7fdlkr/my_cfb_poll_and_methodology/)")

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
        team_total = extra_stats[1][team][0] + extra_stats[1][team][1]

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
    for x in range(1,len(sos_map_copy)):
        lowest_team = min(sos_map_copy.items(), key=operator.itemgetter(1))[0]
        sos_ranking[lowest_team] = x
        del sos_map_copy[lowest_team]

    return (sos_map,sos_ranking)

# Sets up the flair map that will be searchable for the markdown
def generate_flair_map():
    flair_map = {}

    # Reads in the flair map
    with open('flair_list.csv') as flair_csv:
        csvReader = csv.reader(flair_csv)
        for row in csvReader:
            # Formats the flair strings then adds them to the map
            flair_map[row[0]] = "[" + row[0] + "]" + "(#f/" + row[1] + ")"

    return flair_map

def final_rankings_graph(point_map):
    with open('ranking.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(('Team','Points'))
        lowest_points = abs(min(point_map.items(), key=operator.itemgetter(1))[1])
        for key, value in point_map.items():
            writer.writerow([key,value+lowest_points])

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

# Calls my function
if __name__ == '__main__':
    import sys
    main(sys.argv)
