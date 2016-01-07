#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API-DB: flushing $1 documents from api database ..."

	activate_venv api
	python $ESDOC_DIR_API/jobs/run_db_flush.py --project=$1 --source=$2

    log "API-DB: flushed $1 documents from api database"
}

# Invoke entry point.
main $1 $2