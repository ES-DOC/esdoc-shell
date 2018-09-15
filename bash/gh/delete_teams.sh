#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "GITHUB : deleting institutional teams ..."

	activate_venv
	python $ESDOC_DIR_BASH/gh/delete_teams.py

	log "GITHUB : institutional teams deleted"
}

# Invoke entry point.
main $1
