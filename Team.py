import sqlite3
import Game

conn = sqlite3.connect('poll.db')
c = conn.cursor()

class Team():
    def __init__(self, name=None):
        self.games   = []
        self.flair   = None

        if name:
            self.name       = name
            self.elo        = 1500

            # Insert the team into the database for easier sorting at the end
            c.execute('''INSERT INTO Teams (name, elo)
                      VALUES (?, ?);''', (name, 1500))
            self.db_id = c.lastrowid
        else:
            self.name       = 'Not FBS'
            self.elo        = 1100
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

    def set_flair(self, flair)
        self.flair = flair

    def set_elo(self, elo):
        self.elo = elo

    ### Utility Methods
    def add_game(self, game):
        self.games.append(game)
        self.elo = elo
        c.execute('''UPDATE Teams
                        SET elo = ?
                      WHERE id = ?;''', (elo, self.db_id))

    def get_record(self):
        wins  = 0
        loses = 0
        for game in self.games:
            if game.did_team_win(self):
                wins = wins + 1
            else:
                loses = loses + 1

        return [wins, loses]

    # TODO: Figure out a better way of fetching elo. Should I update the ranking to the CSV? Or make a view? Ask Stephen.
    def get_sos(self):
        for game in self.games:
            game.get_opponent(self)

    # TODO: Write this
    def get_sos_rank(self):
        pass