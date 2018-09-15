#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "GITHUB : listing institutional teams ..."

	activate_venv
	python $ESDOC_DIR_BASH/gh/list_teams.py

	log "GITHUB : institutional teams listed"
}

# Invoke entry point.
main $1
