#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API-DB: adding institute to API database ..."
	activate_venv api
	python $ESDOC_DIR_API/jobs/run_db_insert_institute.py --name=$1
    log "API-DB: added institute to API database"
}

# Invoke entry point.
main $1
