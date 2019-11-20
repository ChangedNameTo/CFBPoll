import sqlite3, csv

conn = sqlite3.connect('poll.db')
c    = conn.cursor()
spread_csv_string = 'backtesting.csv'

c.execute('''SELECT g.id AS game_id,
       th.name AS home_team,
       round(th.elo,2) AS home_elo,
       g.home_score AS home_score,
       ta.name AS away_team,
       round(ta.elo,2) AS away_elo,
       g.away_score AS away_score,
       abs(g.home_score - g.away_score) as observed_spread,
       round((abs(th.elo - ta.elo) / 10),2) as predicted_spread,
       round(abs(th.elo - ta.elo),2) as elo_diff
  FROM Games g
  JOIN Teams th ON g.home_id = th.id
  JOIN Teams ta ON g.away_id = ta.id;''')

rows = c.fetchall()

with open(spread_csv_string, 'w') as spread_csv:
    writer = csv.writer(spread_csv, delimiter=',',quoting=csv.QUOTE_MINIMAL)
    writer.writerow(('Game ID','Home','Home Elo','Home Score','Away','Away Elo','Away Score','Obs. Spread','Pred. Spread','Elo Diff.'))

    writer.writerows(rows)