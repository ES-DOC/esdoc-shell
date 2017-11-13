#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "GITHUB : initializing institutional teams ..."

	activate_venv
	python $ESDOC_HOME/bash/gh/init_teams.py

	log "GITHUB : institutional teams initialized"
}

# Invoke entry point.
main $1
