============================
ES-DOC shell - api (web service) commands
============================

esdoc-api
----------------------------

Runs web service in interactive terminal session.

esdoc-api-daemons-init
----------------------------

Initialises & launches API daemon processes.

esdoc-api-daemons-kill
----------------------------

Terminates all API daemon processes.

esdoc-api-daemons-reset-logs
----------------------------

Deletes all API daemon related logs.

esdoc-api-daemons-status
----------------------------

Display status of all API daemon processes.

esdoc-api-daemons-update-config
----------------------------

Updates API daemon process supervisord config file.

esdoc-api-daemons-update-config-for-debug
----------------------------

Updates API daemon process supervisord config file with a file that ensures all logging output is immediately written.

esdoc-api-db-index
----------------------------

Scans archived documents and populates facet database tables.

esdoc-api-db-index-reset
----------------------------

Deletes all facet database tables entries and then reindexes.

esdoc-api-db-ingest
----------------------------

Ingests archived documents into the database.

esdoc-api-db-insert-institute
----------------------------

Inserts an entry into the institute database table.

esdoc-api-db-insert-project
----------------------------

Inserts an entry into the project database table.

esdoc-api-db-install
----------------------------

Installs a new database upon the database server.

esdoc-api-db-reset
----------------------------

Uninstalls existing database from the database server and then installs a new database upon database server.

esdoc-api-db-uninstall
----------------------------

Uninstalls existing database from database server.

esdoc-api-db-write-comparator-setup-data
----------------------------

Writes comparator web page setup data to: $ESDOC_HOME/repos/esdoc-static/data.

esdoc-api-db-write-facets
----------------------------

Writes dumps of document facets to : $ESDOC_HOME/repos/esdoc-static/data.

esdoc-api-db-write-stats
----------------------------

Writes statistics of documents indexed within the database.

