#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API-DB: adding project to API database ..."
	activate_venv api
	python $DIR_API/jobs/run_db_insert_project.py --name=$1 --description=$2 --homepage=$3
    log "API-DB: added project to API database"
}

# Invoke entry point.
main $1 $2 $3
