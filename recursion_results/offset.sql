-- Calculate the histogram of recursion offset from main().

-- This view swaps recursion.depth with the offset from the bottom of the
-- stack (which usually means distance from main()).
CREATE TEMPORARY VIEW recursion_with_offset AS
SELECT crash_id,
       crash.stack_length - (depth + length) as offset,
       length
FROM recursion JOIN crash ON crash_id = crash.id;

SELECT offset, COUNT(*) as count
FROM recursion_with_offset
GROUP BY offset;
