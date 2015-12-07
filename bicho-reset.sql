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


SELECT url FROM attachments WHERE name LIKE '%Stacktrace%';

SELECT url FROM attachments WHERE name LIKE 'Stacktrace%'; -- prevents multi-thread Stacktraces