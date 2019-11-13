import sqlite3
import numpy as np

import Game

conn = sqlite3.connect('poll.db', timeout=30)
c    = conn.cursor()

class Team():
    def __init__(self, name=None, elo=1500, conference_id=None, conference_name="CFB"):
        self.games   = []
        self.flair   = None

        self.name       = name
        self.elo        = elo
        self.conference_id = conference_id
        self.conference_name = conference_name
        self.sos        = 1500

        # Insert the team into the database for easier sorting at the end
        c.execute('''INSERT INTO Teams (name, elo, sos, conference_id)
                    VALUES (?, ?, ?, ?);''', (self.name, self.elo, self.sos, self.conference_id))
        conn.commit()
        self.db_id = c.lastrowid

    def expected_outcome(self, other_rating,predict=False, home=True):
        if predict:
            return (1 / ( 1 + 10**( ( other_rating - (self.elo + 25) ) / 400 ) ) )
        else:
            if (home):
                return (1 / ( 1 + 10**( ( other_rating - (self.elo + 25) ) / 400 ) ) )
            else:
                return (1 / ( 1 + 10**( ( other_rating - (self.elo - 25) ) / 400 ) ) )

    ### Getters/Setters
    def get_name(self):
        return self.name

    def get_conference_name(self):
        return self.conference_name

    def is_p5(self):
        return self.conference_name in [
            'SEC West',
            'Big 10 East',
            'Big 12',
            'Big 10 West',
            'SEC East',
            'PAC 12 North',
            'ACC Atlantic',
            'PAC 12 South',
            'ACC Coastal'
        ]

    def get_db_id(self):
        return self.db_id

    def get_elo(self):
        return self.elo

    def get_flair(self):
        return self.flair

    def set_flair(self, flair):
        if self.ignore_action():
            self.flair = flair

    def set_elo(self, elo):
        if self.ignore_action():
            self.elo = elo
            c.execute('''UPDATE Teams
                            SET elo = ?
                        WHERE id = ?;''', (self.elo, self.db_id))
            conn.commit()

    def set_sos(self):
        if self.ignore_action():
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
        if self.ignore_action():
            self.sos_rank = sos_rank

    def get_rank(self):
        return self.rank

    def set_rank(self, rank, week):
        if self.ignore_action():
            self.rank = rank
            c.execute('''INSERT INTO TeamWeeks (team_id,rank,week)
                            VALUES (?, ?, ?);''',(self.db_id,rank,week))
            conn.commit()

    ### Utility Methods
    def add_game(self, game):
        if self.ignore_action():
            self.games.append(game)

    def ignore_action(self):
        return self.name != "Not D1"

    def get_record(self):
        if self.ignore_action():
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
        # FIX ME NOW
        return 'N/A'

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