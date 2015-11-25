#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API-DB: uningesting documents from api database ..."
	activate_venv api
	python $ESDOC_DIR_API/jobs/run_db_uningest.py --project=$1 --source=$2
    log "API-DB: uningested documents from api database"
}

# Invoke entry point.
main $1 $2
