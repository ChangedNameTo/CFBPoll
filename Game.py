import math
import sqlite3

import Team

from Constants import *

conn = sqlite3.connect('poll.db')
c    = conn.cursor()


#TODO: Convert this to be FinishedGame so that I can make this a subclass of the parent "Game"
class Game:
    def __init__(self, home, home_score, away, away_score, site=None):
        self.home           = home
        self.home_score     = int(home_score)
        self.home_elo_delta = None
        self.away           = away
        self.away_score     = int(away_score)
        self.away_elo_delta = None
        self.site           = site

        # Insert the game into the DB
        c.execute('''INSERT INTO Games (home_id, home_score, home_elo_delta, away_id, away_score, away_elo_delta)
                          VALUES (?, ?, ?, ?, ?, ?);''', (home.get_db_id(), self.home_score, None, away.get_db_id(), self.away_score, None))
        conn.commit()
        self.db_id          = c.lastrowid

    ### Getters and Setters
    def get_home(self):
        return self.home

    def get_away(self):
        return self.away

    def get_opponent(self, team):
        if team == self.home:
            return  self.away
        else:
            return  self.home

    ### Utility Methods
    # The obvious corollary of did away win
    def _is_home_win(self):
        return self.home_score > self.away_score

    def _is_away_win(self):
        return self.home_score < self.away_score

    def did_team_win(self, team):
        if(team == self.home and self._is_home_win()):
            return True

        if(team == self.home and self._is_away_win()):
            return False

        if(team == self.away and self._is_away_win()):
            return True

        if(team == self.away and self._is_home_win()):
            return False

    def _home_elo_score(self):
        if self._is_home_win():
            return 1
        else:
            return 0

    def _away_elo_score(self):
        if self._is_home_win():
            return 0
        else:
            return 1

    # Calculates a multiplier for the margin of victory, works as a scaling factor for when teams get blown out by much better opponents
    def _mov_multiplier(self):
        log_part = math.log(abs(self.home_score - self.away_score))

        if self._is_home_win():
            subtracted = (self.away.get_elo() - self.home.get_elo())
        else:
            subtracted = (self.home.get_elo() - self.away.get_elo())

        multiplied_part =  ( 2.2 / ( ( subtracted ) * 0.001 + 2.2 ) )

        return log_part * multiplied_part

    # Takes the game object and uses it to update the elos of the teams
    def process_game(self):
        self.home.add_game(self)
        self.away.add_game(self)

        home_elo = self.home.get_elo()
        away_elo = self.away.get_elo()

        # Home field advantage accounts for a 2.5 increase in expected score according to Sagarin and accounted for here
        expected_home = self.home.expected_outcome(away_elo, False, True)
        expected_away = self.away.expected_outcome(home_elo, False, False)

        mov_multiplier = self._mov_multiplier()

        new_home_elo = self.home.get_elo() + K_VALUE * (self._home_elo_score() - expected_home) * mov_multiplier
        new_away_elo = self.away.get_elo() + K_VALUE * (self._away_elo_score() - expected_away) * mov_multiplier

        if self._is_home_win():
            new_home_elo = max(new_home_elo, home_elo)
        else:
            new_away_elo = max(new_away_elo, away_elo)

        self.home_elo_delta = new_home_elo - home_elo
        self.away_elo_delta = new_away_elo - away_elo

        c.execute('''UPDATE Games
                        SET home_elo_delta = ?,
                            away_elo_delta = ?
                      WHERE id = ?;''', (self.home_elo_delta, self.away_elo_delta, self.db_id))
        conn.commit()

        self.home.set_elo(new_home_elo)
        self.away.set_elo(new_away_elo)

        self.home.set_sos()
        self.away.set_sos()