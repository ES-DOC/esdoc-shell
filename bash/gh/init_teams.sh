#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "GITHUB : initializing institutional teams ..."

	activate_venv
	python $ESDOC_DIR_BASH/gh/init_teams.py

	log "GITHUB : institutional teams initialized"
}

# Invoke entry point.
main $1
