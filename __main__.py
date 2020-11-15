import pandas as pd

from calculate_srs import calculate_srs

for year in range(2011,2020):
    in_file_path = 'data/{}/games.csv'.format(year)
    out_file_path = 'data/{}/processed_srs.csv'.format(year)

    year_ranking = calculate_srs(in_file_path)
    year_ranking.to_csv(out_file_path)