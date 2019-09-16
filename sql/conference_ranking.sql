  SELECT c.name, round(AVG(t.elo), 2) as average
    FROM Conferences c
    JOIN Teams t ON t.conference_id = c.id
   WHERE c.p5 = 1
GROUP BY c.name
ORDER BY average DESC;