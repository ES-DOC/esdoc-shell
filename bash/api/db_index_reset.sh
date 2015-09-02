#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API-DB: resetting and indexing document facets ..."
	activate_venv api
	python $ESDOC_DIR_API/jobs/run_db_index_reset.py
    log "API-DB: reset and indexed document facets"
}

# Invoke entry point.
main
