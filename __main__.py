import pandas as pd
import numpy as np
import cfbd
import plotly.express as px
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
WEEK      = 8
RUN_SCRAPER = True # Run this if the values in the csvs are out of date

# Value Constants - Tweak the poll outputs.
# My default values are derived using the research contained in the /research directory.
START_YEAR = 2010 
TESTING = False # Set this to false if you care about poll output. 
K_VALUE = 19
HFA = 30 # Raw output is 3.04, converted to elo is 30.4. Rounds down to the whole number.
FCS_ELO = 1204 # FCS Teams lose by, on average, 29.6 points. Converted to elo, 296. Average FBS team is 1500, so 1204 = 1500 - 296
MEAN_REVERSION = 0.446153846153846 

# Dependent Variable
D_V = 'k_value'
LOW_D_V = 16
HIGH_D_V = 24
STEPS = 11

class Execution:
    def build_options(self, iter_d_v=None):
        self.options = {
            'start_year':START_YEAR,
            'testing':TESTING,
            'k_value':K_VALUE,
            'hfa':HFA,
            'fcs_elo':FCS_ELO,
            'mean_reversion':MEAN_REVERSION,
            'end_year':YEAR,
            'week':WEEK
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
            with alive_bar((STEPS * (YEAR + 1 - START_YEAR))) as bar:
                # Set up the output dataframe
                outputs = pd.DataFrame(columns=['iter_year','perc_correct','dv_value'])
                
                for iter_d_v in np.linspace(LOW_D_V, HIGH_D_V, STEPS):
                    testing_games = pd.DataFrame()
                    testing_teams = pd.DataFrame()
                    testing_plays = pd.DataFrame()
                    testing_stats = pd.DataFrame()

                    for iter_year in range(START_YEAR, YEAR + 1):
                        self.build_options(iter_d_v)

                        bar()

                        # Run the cycle
                        polling_cycle = Cycle(self.options, iter_year)
                        results = polling_cycle.run()

                        # Append the iterated dependent variable to our data set
                        results.append(iter_d_v)
                        results_series = pd.Series(results, index=outputs.columns)
                        outputs = outputs.append(results_series, ignore_index=True)

                # Dump the DV outputs to a CSV
                outputs.to_csv('research/D_V.csv')            

                # Print out the DV graph
                fig = px.scatter(outputs, x='dv_value',y='perc_correct')
                fig.write_html('research/dv_test.html')
        else:
            with alive_bar(length=(YEAR + 1 - START_YEAR)) as bar:
                for iter_year in range(START_YEAR, YEAR + 1):
                    self.build_options()

                    bar()
                    polling_cycle = Cycle(self.options, iter_year)
                    output = polling_cycle.run()

execution = Execution()
execution.run()