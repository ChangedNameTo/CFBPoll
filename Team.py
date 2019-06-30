import sqlite3
import numpy as np

import Game

conn = sqlite3.connect('poll.db')
c    = conn.cursor()

class Team():
    def __init__(self, name=None):
        self.games   = []
        self.flair   = None

        if name:
            self.name       = name
            self.elo        = 1500
            self.sos        = 1500

            # Insert the team into the database for easier sorting at the end
            c.execute('''INSERT INTO Teams (name, elo, sos)
                      VALUES (?, ?, ?);''', (name, 1500, 1500))
            conn.commit()
            self.db_id = c.lastrowid
        else:
            self.name       = 'Not FBS'
            self.elo        = 1100
            self.sos        = 1100
            self.db_id      = None

    def expected_outcome(self, other_rating):
            return (1 / ( 1 + 10**( ( other_rating - self.elo ) / 400 ) ))

    ### Getters/Setters
    def get_name(self):
        return self.name

    def get_db_id(self):
        return self.db_id

    def get_elo(self):
        return self.elo

    def get_flair(self):
        return self.flair

    def set_flair(self, flair):
        self.flair = flair

    def set_elo(self, elo):
        self.elo = elo
        c.execute('''UPDATE Teams
                        SET elo = ?
                      WHERE id = ?;''', (elo, self.db_id))

    def set_sos(self):
        avg_array = []
        for game in self.games:
            other_team = game.get_opponent(self)
            avg_array.append(other_team.get_elo())

        sos = int(np.mean(avg_array))
        c.execute('''UPDATE Teams
                        SET sos = ?
                      WHERE id = ?;''', (sos, self.db_id))
        conn.commit()
        self.sos = sos

    def get_sos(self):
        return self.sos

    def get_sos_rank(self):
        return self.sos_rank

    def set_sos_rank(self, sos_rank):
        self.sos_rank = sos_rank

    def get_rank(self):
        return self.rank

    def set_rank(self, rank, week):
        self.rank = rank
        c.execute('''INSERT INTO TeamWeeks (team_id,rank,week)
                          VALUES (?, ?, ?);''',(self.db_id,rank,week))
        conn.commit()

    ### Utility Methods
    def add_game(self, game):
        self.games.append(game)

    def get_record(self):
        wins  = 0
        loses = 0
        for game in self.games:
            if game.did_team_win(self):
                wins = wins + 1
            else:
                loses = loses + 1

        record = "(" + str(wins) + "-" + str(loses) + ")"

        return record

    def get_change(self, week):
        if((week - 1) == 0):
            return 'N/A'
        else:
            c.execute('''SELECT rank
                        FROM TeamWeeks
                        WHERE id = ?
                            AND week = ?;''',(self.db_id, (week - 1)))

            prev_week = c.fetchall()
            current   = self.rank
            change    = current - prev_week

            return change