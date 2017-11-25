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

# Grabs the web page and retreives all of the score data
def grab_web_page():
    score_url = "http://prwolfe.bol.ucla.edu/cfootball/scores.htm"

    # Gets the web page
    request   = urllib.request.Request(score_url)
    response  = urllib.request.urlopen(request)
    page_html = response.read()

    # Pass into the parser, grabs the scores table
    soup        = BeautifulSoup(page_html, 'html.parser')
    score_table = soup.pre.string

    # Returns the scores table
    return score_table

# Takes the passed in score table, returns an array of just scores
def parse_scores(scores):
    # Strips all spaces longer than one
    scores = re.sub(' +', ' ', scores)

    # Splits the score data along every \n char
    parsed_scores = scores.splitlines()

    # Deletes header rows
    del parsed_scores[3]
    del parsed_scores[2]
    del parsed_scores[1]
    del parsed_scores[0]

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

    # Runs a regex on each score to clean up the data
    captured_scores = []
    for score in parsed_scores:
        captures = re.findall("(\d{2}-\w{3}-\d{2})\s([\w+-?\s.&'`?]+)\s+(\d+)\s([\w+-?\s.&'`?]+)\s+(\d+)\s?([\w+\s.?]+)?$", score)

        # If it's fbs only, checks that the team exists in the team array before adding the score
        if(fbs_only):
            if(captures[0][1] not in team_array and captures[0][3] not in team_array):
                continue
            else:
                captured_scores.append(captures[0])
        else:
            captured_scores.append(captures[0])

    # Returns the caputured data
    return captured_scores

# Outputs the data to a csv
def output_data(parsed_scores, output_file):
    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(('Date','Home','Home Score','Away','Away Score','Location if Neutral Site'))
        for score in parsed_scores:
            writer.writerow(score)

# Sets up all of the poll variables
def start_poll(parsed_scores):
    # Sets up the master map that will hold all of the points over poll cycles
    team_point_map = {}
    for team in team_array:
        team_point_map[team] = 0

    y = 1
    for x in range(0,y):
        print("Cycle " + str(x) + " of " + str(y))
        cycle_map = poll_cycle(parsed_scores)

        # Adds this cycle's points to the main map
        for team in team_array:
            team_point_map[team] = cycle_map[team] + team_point_map[team]

    # Sorts the dictionary, popping out each max point team and appending them to the list
    final_ranking = []
    temp_point_map = copy.deepcopy(team_point_map)

    for x in range(0,len(team_point_map)):
        highest_team = max(team_point_map.items(), key=operator.itemgetter(1))[0]
        final_ranking.append(highest_team)
        del team_point_map[highest_team]

    # Creates the opponents map so SoS can be calculated
    extra_stats = extra_stats_parsing(parsed_scores)
    markdown_output(temp_point_map, final_ranking, extra_stats)

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
    debug_poll(tracking_map)
    return cycle_map

# Outputs the team movement over a cycle to see how the movement is happening
def debug_poll(tracking_map):
    with open('debug.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(('Date','Ranks'))
        for key, value in tracking_map.items():
            value.insert(0, key)
            writer.writerow(value)

# Creates a markdown table that can be posting into the reddit comments section
def markdown_output(point_map,final_ranking,extra_stats):
    # Opens the file
    with open("ranking.txt", "w") as file:
        # Writes the table header
        file.write("|Rank|Team|Flair|Record|SoS|SoS Rank|Points|\n")
        file.write("|---|---|---|---|---|---|---|\n")

        # Terminates the ranking after 25
        x = 1

        # Pulls sos for everyone
        output      = calculate_sos(final_ranking,extra_stats)
        sos_map     = output[0]
        sos_ranking = output[1]

        for team in final_ranking:
            # Calculates some things here to pretty up the string itself
            # Looks weird cause python is weird and does weird things
            sos      = str(sos_map[team])
            sos_rank = sos_ranking[team]
            sos_rank = str(sos_rank)
            record   = str(extra_stats[1][team][0]) + "-" + str(extra_stats[1][team][1])

            # Writes to the file
            file.write("|" + str(x) + "|" + team + "|-|" + record + "|" + sos + "|" + sos_rank + "|" + str(point_map[team]) + "|\n")
            x = x + 1

            # Terminates after 25
            if x == 26:
                break

        file.write("\n")

        # Writes out the easiest and hardest SoS
        for key, value in sos_ranking.items():
            if value == 1:
                easiest = key
            if value == 129:
                hardest = key

        file.write("*Easiest SoS:* " + easiest + "\n")
        file.write("\n")
        file.write("*Hardest SoS:* " + hardest + "\n")

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

# Calls my function
if __name__ == '__main__':
    import sys
    main(sys.argv)
