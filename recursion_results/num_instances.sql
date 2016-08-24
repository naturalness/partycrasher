-- Calculates the histogram of the number of instances of recursion per crash.
SELECT num_instances, COUNT(crash) as count
FROM (
    -- Determines how many instances of recursion does each crash have?
    SELECT crash.id as crash, COUNT(crash_id) as num_instances
    FROM crash LEFT JOIN recursion ON crash.id = crash_id
    GROUP BY crash.id
)
GROUP BY num_instances;
