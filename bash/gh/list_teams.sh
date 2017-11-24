#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "GITHUB : listing institutional teams ..."

	activate_venv
	python $ESDOC_HOME/bash/gh/list_teams.py

	log "GITHUB : institutional teams listed"
}

# Invoke entry point.
main $1
