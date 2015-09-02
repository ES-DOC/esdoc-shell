#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API : writing stats ..."
	activate_venv api
	python $ESDOC_DIR_API/jobs/run_write_stats.py --outdir=$ESDOC_DIR_WEB_STATIC/data
    log "API : stats written ---> "$ESDOC_DIR_WEB_STATIC/data
}

# Invoke entry point.
main
