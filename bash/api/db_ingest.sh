#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API-DB: ingesting from pyesdoc archive ..."
	activate_venv api
	python $ESDOC_DIR_API/jobs/run_db_ingest.py
    log "API-DB: ingested from pyesdoc archive"
}

# Invoke entry point.
main
