#!/bin/bash

# ###############################################################
# SECTION: DB FUNCTIONS
# ###############################################################

# ---------------------------------------------------------------
# SUB-SECTION: DB CREATE / DROP HELPER FUNCTIONS
# ---------------------------------------------------------------

# Create db users.
_db_create_users()
{
	log "Creating DB users"

	createuser -U postgres -d -s esdoc_db_admin
	createuser -U esdoc_db_admin -D -S -R esdoc_db_user
}

# Create db.
_db_create()
{
	log "Creating DB"

	createdb -U esdoc_db_admin -e -O esdoc_db_admin -T template0 esdoc_api
	createdb -U esdoc_db_admin -e -O esdoc_db_admin -T template0 esdoc_api_test
}

# Grant db permissions.
_db_grant_permissions()
{
	log "Granting DB permissions"

	psql -U esdoc_db_admin -d esdoc_api -a -f $DIR_BASH/run_db_grant_permissions.sql
	psql -U esdoc_db_admin -d esdoc_api_test -a -f $DIR_BASH/run_db_grant_permissions.sql
}

# Create db users.
_db_drop_users()
{
	log "Deleting DB users"

	dropuser -U esdoc_db_admin esdoc_db_user
	dropuser -U postgres esdoc_db_admin
}

# Drop db.
_db_drop()
{
	log "Dropping DB"

	dropdb -U esdoc_db_admin esdoc_api
	dropdb -U esdoc_db_admin esdoc_api_test
}

# Seed db.
_db_setup()
{
	log "Seeding DB"

	activate_venv api

	python $DIR_JOBS/api/run_db_setup.py
}

# ---------------------------------------------------------------
# SUB-SECTION: DB SHELL COMMANDS
# ---------------------------------------------------------------

# Install db.
run_api_db_install()
{
	log "DB : installing ..."

	_db_create_users
	_db_create
	_db_setup
	_db_grant_permissions

	log "DB : installed ..."
}

# Reset db.
run_api_db_reset()
{
	log "DB : resetting ..."

	run_api_db_uninstall
	run_api_db_install

	log "DB : reset"
}

# Uninstall db.
run_api_db_uninstall()
{
	log "DB : uninstalling ..."

	_db_drop
	_db_drop_users

	log "DB : uninstalled"
}

run_api_db_ingest()
{
    log "DB: ingesting from pyesdoc archive ..."

    declare -a DIRECTORIES=(ingested_error)
    reset_archive_directories $DIRECTORIES

	activate_venv api

	python $DIR_JOBS/api/run_db_ingest.py $1 $2

    log "DB: ingested from pyesdoc archive ..."
}

run_api_db_index()
{
    log "DB: indexing document facets ..."

	activate_venv api

	python $DIR_JOBS/api/run_db_index.py

    log "DB: indexed document facets ..."
}

run_api_db_index_reset()
{
    log "DB: resetting and indexing document facets ..."

	activate_venv api

	python $DIR_JOBS/api/run_db_index_reset.py

    log "DB: reset and indexed document facets ..."
}