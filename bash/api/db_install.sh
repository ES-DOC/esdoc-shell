#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

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
}

# Grant db permissions.
_db_grant_permissions()
{
	log "Granting DB permissions"
	psql -U esdoc_db_admin -d esdoc_api -a -f $ESDOC_DIR_BASH/api/db_grant_permissions.sql
}

# Seed db.
_db_setup()
{
	log "Seeding DB"

    activate_venv api
    python $ESDOC_HOME/bash/api/db_install.py
}

# Main entry point.
main()
{
	log "API-DB : installing ..."

	_db_create_users
	_db_create
	_db_setup
	_db_grant_permissions

	log "API-DB : installed"
}

# Invoke entry point.
main
