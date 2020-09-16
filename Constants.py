#############
# Constants #
#############

# Runtime Constants - Use these to change when or how the poll runs
YEAR      = 2020
WEEK      = 1
RUN_SCRAPER = False # Run this if the values in the csvs are out of date

# Value Constants - Tweak the poll outputs.
# My default values are derived using the research contained in the /research directory.
K_VALUE   = 18
HFA = 30 # Raw output is 3.04, converted to elo is 30.4. Rounds down to the whole number.
FCS_ELO = 1204 # FCS Teams lose by, on average, 29.6 points. Converted to elo, 296. Average FBS team is 1500, so 1204 = 1500 - 296