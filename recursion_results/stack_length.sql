-- Calcultes the histogram of stack lengths.
SELECT stack_length, COUNT(*) as count
FROM crash
GROUP BY stack_length;
