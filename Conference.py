from Constants import *
from statistics import mean

import sqlite3
import numpy as numpy

conn = sqlite3.connect('poll.db', timeout=10)
c    = conn.cursor()

class Conference():
    def __init__(self, name, p5):
        self.name = name
        self.p5 = p5

        c.execute('''INSERT INTO Conferences (name, p5)
                          VALUES (?, ?);''', (self.name, self.p5))
        conn.commit()
        self.db_id = c.lastrowid

    def get_db_id(self):
        return self.db_id

    def set_flair(self, flair):
        self.flair = flair

    def get_flair(self):
        return self.flair

    def mean_reversion(self, team_dict):
        # Get the team ids for this conference
        c.execute('''SELECT name
                       FROM Teams
                      WHERE conference_id = ?;''', (self.db_id,))
        team_names = c.fetchall()

        c.execute('''SELECT AVG(elo)
                       FROM Teams
                      WHERE conference_id = ?;''', (self.db_id,))

        avg_elo = c.fetchall()[0][0]

        for team_name in team_names:
            team_obj = team_dict[team_name[0]]

            prev_elo = team_obj.get_elo()
            adj_elo = ([1500] * WEEK)
            adj_elo.append(prev_elo)
            adj_elo = mean(adj_elo)
            new_elo = mean([avg_elo, adj_elo])
            # new_elo = 1500

            team_obj.set_elo(new_elo)