#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

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
}

# Main entry point.
main()
{
	log "API-DB : uninstalling ..."
	_db_drop
	_db_drop_users
	log "API-DB : uninstalled"
}

# Invoke entry point.
main
