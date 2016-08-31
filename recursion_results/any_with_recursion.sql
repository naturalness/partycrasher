-- Returns random IDs of crashes that are not 2000 stack frames long!
SELECT crash.id as report_id
FROM crash LEFT JOIN recursion ON crash.id = crash_id
WHERE stack_length <> 2000
GROUP BY crash.id
HAVING COUNT(crash_id) >= 1
ORDER BY random()
LIMIT 413;
