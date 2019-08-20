# Import my objects
from Team import Team
from Game import Game

# Import libraries
import urllib.request
from bs4 import BeautifulSoup

# Native libraries
import re, statistics, csv, random, operator, copy, threading, math, os, sqlite3
import numpy as np

conn = sqlite3.connect('poll.db')
c    = conn.cursor()

# Constants
TEAM_LIST = 'util/teams.txt'
SCORE_URL = 'http://prwolfe.bol.ucla.edu/cfootball/scores.htm'

class Ranking():
    def __init__(self, year=2019, week=1):
        # Create the database
        c.execute('''CREATE TABLE IF NOT EXISTS Teams
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                elo INTEGER,
                sos INTEGER
            );''')
        c.execute('''CREATE TABLE IF NOT EXISTS Games
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                home_id INTEGER,
                home_score INTEGER,
                home_elo_delta INTEGER,
                away_id INTEGER,
                away_score INTEGER,
                away_elo_delta INTEGER,
                FOREIGN KEY(home_id) REFERENCES Teams(id)
                FOREIGN KEY(away_id) REFERENCES Teams(id)
            );''')
        c.execute('''CREATE TABLE IF NOT EXISTS TeamWeeks
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER,
                rank INTEGER,
                week INTEGER,
                FOREIGN KEY(team_id) REFERENCES Teams(id)
            );''')
        c.execute('''DELETE FROM Teams;''')
        c.execute('''DELETE FROM Games;''')
        conn.commit()

        # Generate the different utility structures
        self.team_dict  = self.generate_teams()
        self.team_array = list(self.team_dict.keys())
        self.games      = self.parse_games()

        self.week      = week
        self.year      = year

    def _get_team(self, team_name):
        if(team_name in self.team_array):
            return self.team_dict[team_name]
        else:
            return Team()

    def generate_flair_map(self):
        flair_map = {}

        # Reads in the flair map
        with open('util/flair_list.csv') as flair_csv:
            csvReader = csv.reader(flair_csv)
            for row in csvReader:
                # Formats the flair strings then adds them to the map
                flair_map[row[0]] = "[" + row[0] + "]" + "(#f/" + row[1] + ")"

        return flair_map

    def generate_teams(self):
        flair_map = self.generate_flair_map()
        fbs_teams = open(TEAM_LIST, 'r')
        team_dict = {}

        for line in fbs_teams:
            if( len(line) > 0 ):
                team_name            = line.strip("\n")
                new_team             = Team(team_name)
                new_team.set_flair(flair_map[team_name])
                team_dict[team_name] = new_team

        return team_dict

    # Opens a URL containing scores and turns it into an array of Game Objects
    def parse_games(self):
        # Make the request and open the table into a parsable object
        # request = urllib.request.Request(SCORE_URL)
        # response = urllib.request.urlopen(request)
        # page_html = response.read()
        f = open('past_pages/2018_cfb_scores.html', 'r', encoding = "ISO-8859-1")
        page_html = f.read()
        soup = BeautifulSoup(page_html, 'html.parser')
        score_table = soup.pre.string

        scores = re.sub(' +', ' ', score_table)

        # Splits the score data along every \n char
        parsed_scores = scores.splitlines()

        # Deletes header rows
        del parsed_scores[0:3]

        captured_scores = []

        for score in parsed_scores:
            captures = re.findall("(\d{2}-\w{3}-\d{2})\s([\w+-?\s.&'`?]+)\s+(\d+)\s([\w+-?\s.&'`?]+)\s+(\d+)\s?([\w+\s.?]+)?$", score)

            try:
                if(captures[0][1] not in self.team_array and captures[0][3] not in self.team_array):
                    continue
                else:

                    home = self._get_team(captures[0][1])
                    home_score = captures[0][2]
                    away = self._get_team(captures[0][3])
                    away_score = captures[0][4]
                    if captures[0][5]:
                        site = captures[0][5]
                        new_game = Game(home, home_score, away, away_score, site)
                    else:
                        new_game = Game(home, home_score, away, away_score)

                    captured_scores.append(new_game)
            except IndexError as inst:
                pass

        return captured_scores

    def output_games(self):
        with open('csv/' + str(year) + '/week' + week + 'scores.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(('Date','Home','Home Score','Away','Away Score','Location if Neutral Site'))
            for score in self.scores:
                writer.writerow(score)

    def run_poll(self):
        for game in self.games:
            game.process_game()

    def get_results(self):
        c.execute('''SELECT id, name, elo
                       FROM Teams
                   ORDER BY elo DESC;''')
        return c.fetchall()

    def get_elo_array(self, result_array):
        self.elo_array = [x[2] for x in result_array]

    def set_mean_elo(self):
        self.mean = round(statistics.mean(self.elo_array), 2)

    def set_median_elo(self):
        self.median = round(statistics.median(self.elo_array), 2)

    def set_stdev_elo(self):
        self.stdev = round(statistics.stdev(self.elo_array), 2)

    def set_variance_elo(self):
        self.variance = round(statistics.variance(self.elo_array), 2)

    def previous_change(self, result):
        if int(week) > 1:
            f             = open(str(year) + "/week" + str(int(week) - 1) + ".csv", 'r')
            previous_week = csv.reader(f)
        else:
            f             = open(str(int(year) - 1) + "/weekFinal.csv", 'r')
            previous_week = csv.reader(f)

        # TODO: Rewrite this entire section. It's really shit.

    def get_top_25(self):
        c.execute('''SELECT name
                       FROM Teams
                   ORDER BY elo DESC
                      LIMIT 25;''')
        return c.fetchall()

    def get_sos_ranks(self):
        c.execute('''SELECT name, RANK()
                       OVER (
                           ORDER BY sos DESC
                       ) sos_rank
                       FROM Teams;''')

        ranks = c.fetchall()

        for team in ranks:
            team_name = team[0]
            rank      = team[1]

            team_object = self._get_team(team_name)
            team_object.set_sos_rank(rank)

    def get_last_place(self):
        c.execute('''SELECT name
                       FROM Teams
                   ORDER BY elo ASC
                      LIMIT 1;''')
        return c.fetchall()[0][0]

    def generate_this_week(self):
        c.execute('''SELECT name, RANK()
                       OVER (
                           ORDER BY elo DESC
                       ) elo_rank
                       FROM Teams;''')

        ranks = c.fetchall()

        for team in ranks:
            team_name = team[0]
            rank      = team[1]

            team_object = self._get_team(team_name)
            team_object.set_rank(rank, self.week)

    def markdown_output(self):
        try:
            os.remove('ranking.txt')
        except FileNotFoundError as e:
            pass

        with open('ranking.txt', 'w') as file:
            # Writes the table header
            file.write("|Rank|Team|Flair|Record|SoS^^1|SoS Rank|ELO|Change|\n")
            file.write("|---|---|---|---|---|---|---|---|\n")


            # TODO: Rewrite conference ranking
            # conference_ranking(final_ranking, sos_ranking, point_map, True)

            rank = 1
            for team in self.get_top_25():
                # sos      = str(sos_map[team])
                # sos_rank = sos_ranking[team]
                # sos_rank = str(sos_rank)
                # record   = str(extra_stats[1][team][0]) + "-" + str(extra_stats[1][team][1])
                # change   = str(last_week[team])

                team_name = team[0]
                team      = self.team_dict[team_name]
                flair     = team.get_flair()
                elo       = round(team.get_elo(), 2)
                record    = team.get_record()
                sos       = round(team.get_sos(), 2)
                sos_rank  = team.get_sos_rank()
                change    = team.get_change(self.week)

                # # Writes to the file
                file.write("|" + str(rank) + "|" + team_name + "|" + flair + "|" + record + "|" + str(sos) + "|" + str(sos_rank) + "|" + str(elo) + "|" + str(change) + "|\n")
                rank = rank + 1

            # Outputs Georgia Tech's data cause I like them
            file.write("||||||||\n")
            team_name = 'Georgia Tech'
            team      = self.team_dict[team_name]
            rank      = team.get_rank()
            flair     = team.get_flair()
            elo       = round(team.get_elo(), 2)
            record    = team.get_record()
            sos       = round(team.get_sos(), 2)
            sos_rank  = team.get_sos_rank()
            change    = team.get_change(self.week)

            # # Writes to the file
            file.write("|" + str(rank) + "|" + team_name + "|" + flair + "|" + record + "|" + str(sos) + "|" + str(sos_rank) + "|" + str(elo) + "|" + str(change) + "|\n")
            rank = rank + 1

            # Outputs the lowest team too just for fun
            file.write("||||||||\n")
            team_name = self.get_last_place()
            team      = self.team_dict[team_name]
            rank      = team.get_rank()
            flair     = team.get_flair()
            elo       = round(team.get_elo(), 2)
            record    = team.get_record()
            sos       = round(team.get_sos(), 2)
            sos_rank  = team.get_sos_rank()
            change    = team.get_change(self.week)

            # Writes to the file
            file.write("|" + str(rank) + "|" + team_name + "|" + flair + "|" + record + "|" + str(sos) + "|" + str(sos_rank) + "|" + str(elo) + "|" + str(change) + "|\n")

            file.write("\n")

            # TODO: This won't work with the new system either
            # Writes out the easiest and hardest SoS
            # for key, value in sos_ranking.items():
            #     if value == 1:
            #         easiest = key
            #     if value == 129:
            #         hardest = key

            file.write("---\n")
            file.write("\n")
            file.write("**Mean Points:** " + str(self.mean) + "\n")
            file.write("\n")
            file.write("**Median Points:** " + str(self.median) + "\n")
            file.write("\n")
            file.write("**Standard Deviation of Points:** " + str(self.stdev) + "\n")
            file.write("\n")
            file.write("**Variance:** " + str(self.variance) + "\n")
            file.write("\n")
            file.write("---\n")
            file.write("\n")
            # TODO: Gotta update this too
            # file.write("**Hardest SoS:** " + flair_map[easiest] + " " + easiest + "\n")
            # file.write("\n")
            # file.write("**Easiest SoS:** " + flair_map[hardest] + " " + hardest + "\n")
            # file.write("\n")
            file.write("---\n")
            file.write("\n")
            file.write("1: Lower means easier SoS\n")
            file.write("\n")
            file.write("[Explanation of the poll methodology here](https://www.reddit.com/user/TehAlpacalypse/comments/9csiv4/cfb_poll_20_the_elo_update/)\n")
            file.write("\n")
            file.write("[Link to the github repository here](https://github.com/ChangedNameTo/CFBPoll)")

ranking = Ranking()
ranking.run_poll()

result = ranking.get_results()
ranking.get_elo_array(result)
ranking.set_mean_elo()
ranking.set_median_elo()
ranking.set_stdev_elo()
ranking.set_variance_elo()

ranking.generate_this_week()

ranking.get_sos_ranks()

ranking.markdown_output()