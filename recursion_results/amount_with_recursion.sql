-- Returns number crashes with recursion
SELECT COUNT(*) as amount
FROM (SELECT crash.id as report_id
        FROM crash LEFT JOIN recursion ON crash.id = crash_id
    GROUP BY crash.id
      HAVING COUNT(crash_id) >= 1);
