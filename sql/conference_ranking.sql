  SELECT id, name, elo
    FROM Teams
   WHERE conference_id IN (3, 13)
ORDER BY elo DESC