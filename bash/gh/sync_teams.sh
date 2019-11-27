#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "GITHUB : synching "$1" GitHub teams ..."

	activate_venv

	if [ $1 = "cmip5" ]; then
		python $ESDOC_DIR_BASH/gh/sync_teams_cmip5.py
	fi

	if [ $1 = "cmip6" ]; then
		python $ESDOC_DIR_BASH/gh/sync_teams_cmip6.py
	fi

	if [ $1 = "cordex" ]; then
		python $ESDOC_DIR_BASH/gh/sync_teams_cordex.py
	fi

	log "GITHUB : synched "$1" GitHub teams"
}

# Invoke entry point.
main $1
