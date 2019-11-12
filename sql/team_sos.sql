SELECT g.id AS game_id,
       th.name AS home_team,
       ta.name AS away_team,
       th.elo AS home_elo,
       ta.elo AS away_elo
  FROM Games g
  JOIN Teams th ON g.home_id = th.id
  JOIN Teams ta ON g.away_id = ta.id
 WHERE th.name = 'Tulsa'
    OR ta.name = 'Tulsa'