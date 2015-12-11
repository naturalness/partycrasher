TRUNCATE TABLE attachments;
TRUNCATE TABLE changes;
TRUNCATE TABLE comments;
TRUNCATE TABLE issues;
TRUNCATE TABLE issues_ext_launchpad;
TRUNCATE TABLE issues_watchers;
TRUNCATE TABLE people;
TRUNCATE TABLE related_to;
TRUNCATE TABLE supported_trackers;
TRUNCATE TABLE trackers;


DROP TABLE attachments;
DROP TABLE changes;
DROP TABLE comments;
DROP TABLE issues;
DROP TABLE issues_ext_launchpad;
DROP TABLE issues_watchers;
DROP TABLE people;
DROP TABLE related_to;
DROP TABLE supported_trackers;
DROP TABLE trackers;


SELECT url FROM attachments WHERE name LIKE '%Stacktrace%';

SELECT url FROM attachments WHERE name LIKE 'Stacktrace%'; -- prevents multi-thread Stacktraces


SELECT url FROM attachments WHERE name LIKE 'Stacktrace%' INTO OUTFILE '/tmp/stacktraces.txt';

-- wget --wait=2 -i /tmp/stacktraces.txt -x -c --random-wait --no-clobber

-- bug: 125544
-- dupe: 122941
-- id: 86
