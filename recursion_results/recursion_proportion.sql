-- What proportion of the each crash's stack is composed of recursion?
-- Will produce one row per crash!
-- The relative proportion can be computed by calculating:
--   recursion_length / stack_length
-- for each crash.
SELECT crash.id as crash,
       COALESCE(SUM(recursion.length), 0) as recursion_length,
       stack_length
FROM crash LEFT JOIN recursion ON crash.id = crash_id
GROUP BY crash.id;
