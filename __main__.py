# Import the timer functions
import timeit
start = timeit.default_timer()

import pandas as pd
import numpy as np
import cfbd
import os
import math
import datetime as dt
import sys

from alive_progress import alive_bar

# Import my own functions
sys.path.insert(1, './research')
from Cycle import Cycle
from stats_scraping import scrape_stats

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('mode.chained_assignment', None) # Disable this if you have issues. This is to supress a warning in the SOS section of the Team code that is working as intended. 

#############
# Constants #
#############
# Runtime Constants - Use these to change when or how the poll runs
YEAR      = 2020
WEEK      = 6
RUN_SCRAPER = False # Run this if the values in the csvs are out of date

# Value Constants - Tweak the poll outputs.
# My default values are derived using the research contained in the /research directory.
START_YEAR = 2010 
TESTING = False # Set this to false if you care about poll output. 
K_VALUE   = 18
HFA = 30 # Raw output is 3.04, converted to elo is 30.4. Rounds down to the whole number.
FCS_ELO = 1204 # FCS Teams lose by, on average, 29.6 points. Converted to elo, 296. Average FBS team is 1500, so 1204 = 1500 - 296
MEAN_REVERSION = 0.6047 # Calculated the correlation between a previous and current seasons elo across 10 seasons. 60% of a new seasons value is explainable by last season. Use this to seed.

# Dependent Variable
D_V = 'mean_reversion'
LOW_D_V = 0
HIGH_D_V = 1
STEPS = 11

class Execution:
    def build_options(self, iter_d_v=None):
        self.options = {
            'start_year':START_YEAR,
            'testing':TESTING,
            'k_value':K_VALUE,
            'hfa':HFA,
            'fcs_elo':FCS_ELO,
            'mean_reversion':MEAN_REVERSION
        }

        if TESTING:
            self.options[D_V] = iter_d_v

    def run(self):
        # Should we run the scraper? This is controlled in Constants
        if RUN_SCRAPER:
            scrape_stats(WEEK)

        # Is this a testing run or a real run? Testing runs are significantly longer
        if TESTING:
            # Set up the progressbar
            with alive_bar(length=(STEPS * (YEAR + 1 - START_YEAR))) as bar:
                for iter_d_v in np.linspace(LOW_D_V, HIGH_D_V, STEPS):
                    testing_games = pd.DataFrame()
                    testing_teams = pd.DataFrame()
                    testing_plays = pd.DataFrame()
                    testing_stats = pd.DataFrame()

                    for iter_year in range(START_YEAR, YEAR + 1):
                        self.build_options(iter_d_v)

                        bar()
                        polling_cycle = Cycle(self.options, iter_year)
                        output = polling_cycle.run()
        else:
            with alive_bar(length=(YEAR + 1 - START_YEAR)) as bar:
                for iter_year in range(START_YEAR, YEAR + 1):
                    self.build_options()

                    bar()
                    polling_cycle = Cycle(self.options, iter_year)
                    output = polling_cycle.run()

execution = Execution()
execution.run()