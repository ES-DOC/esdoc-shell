#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API-DB: adding institute to API database ..."
	activate_venv api
	python $DIR_API/jobs/run_db_insert_institute.py --name=$1 --description=$2 --country=$3 --homepage=$4
    log "API-DB: added institute to API database"
}

# Invoke entry point.
main $1 $2 $3 $4
