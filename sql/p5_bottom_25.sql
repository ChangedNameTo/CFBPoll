   SELECT t.name AS team,
          round(t.elo, 2) AS elo,
          c.name AS conference
     FROM Teams t
     JOIN Conferences c ON c.id = t.conference_id
    WHERE c.p5 = 1
 ORDER BY elo ASC
    LIMIT 25