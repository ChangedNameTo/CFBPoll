-- WITH average (id, average) AS (
--   SELECT c.id, round(AVG(t.elo), 2)
--     FROM Conferences c
--     JOIN Teams t ON t.conference_id = c.id
--    WHERE c.p5 = 1
-- ),
--      sos (id, sos) AS (
  SELECT c.id, round(AVG(t.sos), 2)
    FROM Conferences c
    JOIN Teams t ON t.conference_id = c.id
   WHERE c.p5 = 1
-- )
--   SELECT c.name, a.average, s.sos
--     FROM Conferences c
--     JOIN average a ON a.id = c.id
--     JOIN sos s ON s.id = c.id
-- GROUP BY c.name
-- ORDER BY a.average DESC;