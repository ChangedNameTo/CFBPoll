from Team import Team
from Game import Game
from Ranking import Ranking

import sqlite3
import numpy as np

conn = sqlite3.connect('poll.db')
c    = conn.cursor()

class Collection():
    def __init__(self, year=2019, week=1):
        c.execute('''CREATE TABLE IF NOT EXISTS TeamCollection
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name
            );''')