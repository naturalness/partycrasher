-- Returns the IDs of all crashes with recursion.
SELECT crash_id
FROM recursion JOIN crash ON crash_id = crash.id
WHERE stack_length = 2000
GROUP BY crash_id;
