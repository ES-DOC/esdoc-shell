#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "GITHUB : testing team membership ..."

	activate_venv
	python $ESDOC_HOME/bash/gh/test_team_membership.py --team=$1 --user=$2

	log "GITHUB : institutional teams initialized"
}

# Invoke entry point.
main $1 $2
