-- Calculates the histogram of recursion length for EVERY instance of
-- recursion found in the database. Note that the the miminum length
-- is 2 for any given instance of recursion.
SELECT length, COUNT(*) as count
FROM recursion
GROUP BY length;
