# College football poll designed and maintained by /u/TehAlpacalypse

# Web Parser
from bs4 import BeautifulSoup
# Grabs the web pages
import urllib.request
# Regexes for stripping and such
import re
# Dumps all of this data to a csv
import csv

# Calls all of the other subordinate functions
def main(args):
    global team_list, fbs_only

    output_file = args[1]
    team_list   = args[2]
    fbs_only    = args[3]

    scores        = grab_web_page()
    parsed_scores = parse_scores(scores)

    output_data(parsed_scores, output_file)

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

# Calls my function
if __name__ == '__main__':
    import sys
    main(sys.argv)
