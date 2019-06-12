import math

import Team

K_VALUE = 15

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
                          VALUES (?, ?, ?, ?, ?, ?);''', (home.get_db_id(), self.home_score, NULL, away.get_db_id(), self.away_score, NULL))
        self.db_id          = c.lastrowid

    ### Getters and Setters
    def get_home(self):
        return self.home

    def get_away(self):
        return self.away

    def get_opponent(self, team):
        if team isinstance home:
            return away
        else:
            return home

    ### Utility Methods
    # The obvious corollary of did away win
    def _is_home_win(self):
        return home_score > away_score

    def did_team_win(self, team):
        return (team isinstance self.home and self._is_home_win()) or (team isinstance self.away and not self._is_home_win())

    def _home_elo_score(self):
        if _is_home_win():
            return 1
        else:
            return 0

    def _away_elo_score(self):
        if _is_home_win():
            return 0
        else:
            return 1

    # Calculates a multiplier for the margin of victory, works as a scaling factor for when teams get blown out by much better opponents
    def _mov_multiplier(self):
        log_part = math.log(abs(self.home_score - self.away_score))

        if _is_home_win():
            subtracted = (self.rating_away - self.rating_home)
        else:
            subtracted = (self.rating_home - self.rating_away)

        multiplied_part =  ( 2.2 / ( ( subtracted ) * 0.001 + 2.2 ) )

        return log_part * multiplied_part

    # Takes the game object and uses it to update the elos of the teams
    def process_game(self):
        home.add_game(self)
        away.add_game(self)

        home_elo = home.get_elo()
        away_elo = away.get_elo()

        expected_home = home.expected_outcome(away_elo)
        expected_away = away.expected_outcome(home_elo)

        mov_multiplier = _mov_multiplier()

        new_home_elo= home_elo + K_VALUE * (_home_elo_score() - expected_home) * mov_multiplier
        new_away_elo = away_elo + K_VALUE * (_away_elo_score() - expected_away) * mov_multiplier

        if _is_home_win():
            new_home_elo = max(new_home_elo, home_elo)
        else:
            new_away_elo = max(new_away_elo, away_elo)

        self.home_elo_delta = new_home_elo - home_elo
        self.away_elo_delta = new_away_elo - away_elo

        c.execute('''UPDATE Games
                        SET home_elo_delta = ?,
                            away_elo_delta = ?
                      WHERE id = ?;''', (self.home_elo_delta, self.away_elo_delta))

        home.set_elo(new_home_elo)
        away.set_elo(new_away_elo)