SELECT g.id AS game_id,
       th.name AS home_team,
       th.elo AS home_elo,
       g.home_score AS home_score,
       ta.name AS away_team,
       ta.elo AS away_elo,
       g.away_score AS away_score,
       abs(g.home_score - g.away_score) as observed_spread,
       (abs(th.elo - ta.elo) / 10) as predicted_spread
  FROM Games g
  JOIN Teams th ON g.home_id = th.id
  JOIN Teams ta ON g.away_id = ta.id