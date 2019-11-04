  SELECT name
    FROM Teams
   WHERE name NOT LIKE 'Not FBS'
ORDER BY elo ASC
   LIMIT 1;