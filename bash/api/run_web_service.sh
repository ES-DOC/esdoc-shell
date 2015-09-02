#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API : running ..."
	activate_venv api
	python $ESDOC_DIR_API/jobs/run_api.py
}

# Invoke entry point.
main
