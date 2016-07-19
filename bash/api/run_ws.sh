#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API : running ..."

	activate_venv api
    python $ESDOC_HOME/bash/api/run_ws.py
}

# Invoke entry point.
main
