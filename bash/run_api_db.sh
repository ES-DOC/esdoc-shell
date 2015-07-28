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

	python $DIR_API/jobs/run_db_setup.py
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
	# _run_archive_delete_ingest_files

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

	activate_venv api
	python $DIR_API/jobs/run_db_ingest.py

    log "DB: ingested from pyesdoc archive ..."
}

run_api_db_index()
{
    log "DB: indexing document facets ..."

	activate_venv api

	python $DIR_API/jobs/run_db_index.py

    log "DB: indexed document facets ..."
}

run_api_db_index_reset()
{
    log "DB: resetting and indexing document facets ..."

	activate_venv api

	python $DIR_API/jobs/run_db_index_reset.py

    log "DB: reset and indexed document facets ..."
}

run_api_db_facet_dump()
{
    log "DB: dumping facets to file system ..."

	activate_venv api

	python $DIR_API/jobs/run_db_facet_dump.py --output-dir=$DIR_WEB_STATIC/data

    log "DB: reset and indexed document facets ..."
}

run_api_db_insert_project()
{
    log "DB: adding project to API database ..."

	activate_venv api

	python $DIR_API/jobs/run_db_insert_project.py --name=$1 --description=$2 --homepage=$3

    log "DB: added project to API database ..."
}

run_api_db_insert_institute()
{
    log "DB: adding institute to API database ..."

	activate_venv api

	python $DIR_API/jobs/run_db_insert_institute.py --name=$1 --description=$2 --country=$3 --homepage=$4

    log "DB: added institute to API database ..."
}