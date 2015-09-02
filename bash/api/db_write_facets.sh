#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API-DB: dumping facets to file system ..."
	activate_venv api
	python $ESDOC_DIR_API/jobs/run_db_facet_dump.py --output-dir=$ESDOC_DIR_WEB_STATIC/data
    log "API-DB: dumped facets to file system"
}

# Invoke entry point.
main
