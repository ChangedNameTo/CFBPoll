# Import my objects
from Team import Team
from Game import Game
from Conference import Conference
from Constants import YEAR, WEEK, SEED_DATE, START_DATE, END_DATE, SCHEDULE_URL, SCORE_URL
from Dates import wolfe_to_date
from Betting import Betting

# Import libraries
import urllib.request
from bs4 import BeautifulSoup

# Native libraries
import re, statistics, csv, random, operator, copy, threading, math, os, sqlite3, calendar
import datetime
from datetime import timedelta
import numpy as np

conn = sqlite3.connect('poll.db')
c    = conn.cursor()

class Ranking():
    def __init__(self, year=2019, week=1):
        # Clears out the db
        c.execute('''DROP TABLE IF EXISTS Conferences;''')
        c.execute('''DROP TABLE IF EXISTS Teams;''')
        c.execute('''DROP TABLE IF EXISTS Games;''')
        c.execute('''DROP TABLE IF EXISTS TeamWeeks;''')
        c.execute('''DROP TABLE IF EXISTS Weeks;''')

        # Create the database
        c.execute('''CREATE TABLE IF NOT EXISTS Conferences
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                p5 BOOLEAN
            );''')
        c.execute('''CREATE TABLE IF NOT EXISTS Teams
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                elo FLOAT,
                sos INTEGER,
                conference_id INTEGER,
                FOREIGN KEY(conference_id) REFERENCES Conferences(id)
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
        c.execute('''CREATE TABLE IF NOT EXISTS Weeks
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_date INTEGER,
                end_date INTEGER
            );''')
        conn.commit()

        self.team_dict       = {}
        self.conference_dict = {}

        flair_map            = self.generate_flair_map()

        f = open('util/seeds/2019SeedFile.csv')
        seed_csv = csv.reader(f)

        for line in seed_csv:
            name       = line[0]
            elo        = float(line[1])
            conference = line[2]
            p5         = (line[3] == 'True')

            if(conference not in self.conference_dict.keys()):
                new_conf = Conference(conference, p5)
                new_conf.set_flair(flair_map[conference])
                self.conference_dict[conference] = new_conf

            conf_id = self.conference_dict[conference].get_db_id()

            new_team = Team(name, elo, conf_id, conference)
            if new_team.ignore_action():
                if(name in flair_map.keys()):
                    new_team.set_flair(flair_map[name])
                else:
                    new_team.set_flair(flair_map['CFB'])
            self.team_dict[name] = new_team

        # Generate the different utility structures
        self.team_array = list(self.team_dict.keys())
        self.conf_array = list(self.conference_dict.keys())
        self.games      = self.parse_games()

        self.week      = week
        self.year      = year

    def _get_team(self, team_name):
        if team_name in self.team_array:
            return self.team_dict[team_name]
        else:
            return self.team_dict['Not D1']

    def generate_weeks(self):
        year, month, day = wolfe_to_date(SEED_DATE)
        curr_date = datetime.date(year, month, day)
        end_date = datetime.date(2020, 1, 14)
        while(curr_date < end_date):
            s = curr_date.strftime('%Y-%m-%d')
            curr_date = curr_date + timedelta(weeks=1)
            e = curr_date.strftime('%Y-%m-%d')
            c.execute('''INSERT INTO Weeks (start_date, end_date)
                              VALUES (date(?), date(?));''',(s, e))
            conn.commit()

    def generate_flair_map(self):
        flair_map = {}

        # Reads in the flair map
        with open('util/csvs/flair_list.csv') as flair_csv:
            csvReader = csv.reader(flair_csv)
            for row in csvReader:
                # Formats the flair strings then adds them to the map
                flair_map[row[0]] = "[" + row[0] + "]" + "(#f/" + row[1] + ")"

        # Reads in the flair map
        with open('util/csvs/conference_flair.csv') as flair_csv:
            csvReader = csv.reader(flair_csv)
            for row in csvReader:
                # Formats the flair strings then adds them to the map
                flair_map[row[0]] = "[" + row[0] + "]" + "(#l/" + row[1] + ")"

        return flair_map

    # Adjusts all teams relative to their divsion's mean elo when seeding
    def mean_reversion(self):
        for conference in self.conf_array:
            conf_object = self.conference_dict[conference]
            conf_object.mean_reversion(self.team_dict)

    # Opens a URL containing scores and turns it into an array of Game Objects
    def parse_games(self):
        # Make the request and open the table into a parsable object
        request = urllib.request.Request(SCORE_URL)
        response = urllib.request.urlopen(request)
        page_html = response.read()
        # f = open('past_pages/2018_cfb_scores.html', 'r', encoding = "ISO-8859-1")
        # page_html = f.read()
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
            except IndexError:
                pass

        return captured_scores

    def parse_future(self):
        # Make the request and open the table into a parsable object
        request = urllib.request.Request(SCHEDULE_URL)
        response = urllib.request.urlopen(request)
        page_html = response.read()
        # f = open('past_pages/2018_cfb_scores.html', 'r', encoding = "ISO-8859-1")
        # page_html = f.read()
        soup = BeautifulSoup(page_html, 'html.parser')
        scores = soup.pre.string

        # scores = re.sub(' +', ' ', score_table)

        # Splits the score data along every \n char
        future_games = scores.splitlines()

        # Deletes header rows
        del future_games[0:3]

        week_csv_string = 'csv/' + str(YEAR) + '/week_' + str(WEEK) + '_predictions.csv'
        with open(week_csv_string, 'w') as week_csv:
            writer = csv.writer(week_csv, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(('Date','Home','Away','Predicted Winner', 'Odds'))

            # Hacky way to continue....
            found_present = False
            for game in future_games:
                captures = re.findall("(\d{2}-\w{3}-\d{2})\s([\w\s'-.&`]*?)\s{2,}([\w\s'-.&`]*?)\s{2,}", game)
                try:
                    if(found_present == False):
                        if(captures[0][0] != START_DATE):
                            continue
                        else:
                            found_present = True

                    #TODO: Make this use calendar and datetime to do more intelligent bounding
                    if(captures[0][0] == END_DATE):
                        break

                    if(captures[0][1] not in self.team_array and captures[0][2] not in self.team_array):
                        continue
                    else:
                        date = captures[0][0]

                        home = self._get_team(captures[0][1])
                        away = self._get_team(captures[0][2])

                        home_elo = round(home.get_elo(), 2)
                        away_elo = round(away.get_elo(), 2)

                        winner = home if home_elo > away_elo else away
                        loser  = home if home_elo < away_elo else away

                        home_string   = home.get_name() + ' (' + str(home_elo) + ')'
                        away_string   = away.get_name() + ' (' + str(away_elo) + ')'

                        winner_string = winner.get_name()
                        winner_odds = round((winner.expected_outcome(loser.get_elo(), True) * 100), 2)

                        writer.writerow((date,home_string, away_string, winner_string, winner_odds))
                except IndexError:
                    pass

    def run_poll(self):
        for game in self.games:
            game.process_game()

    def get_results(self):
        c.execute('''SELECT id, name, elo
                       FROM Teams
                      WHERE name NOT LIKE 'Not D1'
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

    def get_top_25(self):
        c.execute('''SELECT name
                       FROM Teams
                      WHERE name NOT LIKE 'Not D1'
                   ORDER BY elo DESC
                      LIMIT 25;''')
        return c.fetchall()

    def get_sos_ranks(self):
        c.execute('''SELECT name, RANK()
                       OVER (
                           ORDER BY sos DESC
                       ) sos_rank
                       FROM Teams
                      WHERE name NOT LIKE 'Not D1';''')

        ranks = c.fetchall()

        for team in ranks:
            team_name = team[0]
            rank      = team[1]

            team_object = self._get_team(team_name)
            team_object.set_sos_rank(rank)

    def get_last_place(self):
        c.execute('''SELECT name
                       FROM Teams
                      WHERE name NOT LIKE 'Not D1'
                   ORDER BY elo ASC
                      LIMIT 1;''')
        return c.fetchall()[0][0]

    def generate_this_week(self):
        c.execute('''SELECT name, RANK()
                       OVER (
                           ORDER BY elo DESC
                       ) elo_rank
                       FROM Teams
                      WHERE name NOT LIKE 'Not D1';''')

        ranks = c.fetchall()

        for team in ranks:
            team_name = team[0]
            rank      = team[1]

            team_object = self._get_team(team_name)
            team_object.set_rank(rank, self.week)

    def markdown_output(self):
        try:
            os.remove('ranking.txt')
        except FileNotFoundError:
            pass

        with open('ranking.txt', 'w') as file:
            # Writes the table header
            file.write("|Rank|Team|Flair|Record|Elo|SoS^^1|SoS Rank|Change|\n")
            file.write("|---|---|---|---|---|---|---|---|\n")

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
                file.write("|" + str(rank) + "|" + team_name + "|" + flair + "|" + record + "|" + str(elo) + "|" + str(sos) + "|" + str(sos_rank) + "|" + str(change) + "|\n")
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
            file.write("|" + str(rank) + "|" + team_name + "|" + flair + "|" + record + "|" + str(elo) + "|" + str(sos) + "|" + str(sos_rank) + "|" + str(change) + "|\n")
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
            file.write("|" + str(rank) + "|" + team_name + "|" + flair + "|" + record + "|" + str(elo) + "|" + str(sos) + "|" + str(sos_rank) + "|" + str(change) + "|\n")

            file.write("\n")

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
            file.write("---\n")
            file.write("\n")
            file.write("1: SoS is the average of all opponents at time of ranking, not at time of playing. I don't believe in the 'ranked win' paradigm, if my poll supported it yet I would randomize the schedule.\n")
            file.write("\n")
            file.write("[Explanation of the poll methodology here](https://www.reddit.com/user/TehAlpacalypse/comments/dwfsfi/cfb_poll_30_oops/)\n")
            file.write("\n")
            file.write("[Link to the github repository here](https://github.com/ChangedNameTo/CFBPoll)")

    def conference_output(self):
        try:
            os.remove('conference.txt')
        except FileNotFoundError:
            pass

        with open('conference.txt', 'w') as file:
            # Writes the table header
            file.write("|Rank|Conference|Flair|ELO|\n")
            file.write("|---|---|---|---|\n")

            c.execute('''SELECT c.name, round(AVG(t.elo), 2) as average
                        FROM Conferences c
                        JOIN Teams t ON t.conference_id = c.id
                    GROUP BY c.name
                    ORDER BY average DESC;''')

            ranks = c.fetchall()

            rank = 1
            for conference in ranks:
                name = conference[0]
                conf_obj = self.conference_dict[name]
                flair = conf_obj.get_flair()
                elo  = conference[1]

                file.write("|" + str(rank) + "|" + name + "|" + flair + "|" + str(elo) + "|\n")
                rank = rank + 1

    def output_week_csv(self, result):
        week_csv_string = 'csv/' + str(YEAR) + '/week_' + str(WEEK) + '.csv'
        with open(week_csv_string, 'w') as week_csv:
            writer = csv.writer(week_csv, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(('Rank','Team','Record','ELO','SoS','SoS Rank','Change','Conference','Is P5'))

            rank = 1
            for team in result:
                name     = team[1]
                team_obj = self.team_dict[name]
                record   = team_obj.get_record()
                elo      = round(team_obj.get_elo(),2)
                sos      = round(team_obj.get_sos(),2)
                sos_rank = team_obj.get_sos_rank()
                change   = team_obj.get_change(WEEK)
                conference   = team_obj.get_conference_name()
                is_p5 = team_obj.is_p5()

                writer.writerow((rank, name, record, elo, sos, sos_rank, change, conference, is_p5))
                rank = rank + 1

    def conference_ranking(self):
        c.execute('''SELECT c.name, round(AVG(t.elo), 2) as average
                       FROM Conferences c
                       JOIN Teams t ON t.conference_id = c.id
                   GROUP BY c.name
                   ORDER BY average DESC;''')

        ranks = c.fetchall()

        week_conference_csv = 'csv/' + str(YEAR) + '/week_' + str(WEEK) + '_conferences.csv'
        with open(week_conference_csv, 'w') as week_csv:
            writer = csv.writer(week_csv, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(('Rank','Conference','Elo'))

            rank = 1
            for conference in ranks:
                name = conference[0]
                elo  = conference[1]

                writer.writerow((rank, name, elo))
                rank = rank + 1


ranking = Ranking()
ranking.generate_weeks()
ranking.mean_reversion()
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

ranking.output_week_csv(result)
ranking.conference_ranking()
ranking.conference_output()

# Prediction time
ranking.parse_future()