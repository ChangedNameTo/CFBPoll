  SELECT id, round(name, 2), sos
    FROM Teams
   WHERE conference_id = 9
ORDER BY elo DESC;