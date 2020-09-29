#############
# Constants #
#############

# Runtime Constants - Use these to change when or how the poll runs
YEAR      = 2020
WEEK      = 4
RUN_SCRAPER = False # Run this if the values in the csvs are out of date

# Researching constants
TESTING = True # Set this to false if you care about poll output. 

# Value Constants - Tweak the poll outputs.
# My default values are derived using the research contained in the /research directory.
START_YEAR = 2010 
K_VALUE   = 18
HFA = 30 # Raw output is 3.04, converted to elo is 30.4. Rounds down to the whole number.
FCS_ELO = 1204 # FCS Teams lose by, on average, 29.6 points. Converted to elo, 296. Average FBS team is 1500, so 1204 = 1500 - 296
MEAN_REVERSION = 0.6047 # Calculated the correlation between a previous and current seasons elo across 10 seasons. 60% of a new seasons value is explainable by last season. Use this to seed.