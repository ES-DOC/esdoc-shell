#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "GITHUB : deleting institutional teams ..."

	activate_venv
	python $ESDOC_HOME/bash/gh/delete_teams.py

	log "GITHUB : institutional teams deleted"
}

# Invoke entry point.
main $1
