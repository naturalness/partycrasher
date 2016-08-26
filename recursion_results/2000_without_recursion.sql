-- Returns the IDs of all crashes with recursion.
SELECT crash.id
FROM crash LEFT JOIN recursion ON crash.id = crash_id
WHERE stack_length = 2000
GROUP BY crash.id
HAVING COUNT(crash_id) = 0;
