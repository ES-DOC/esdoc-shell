#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "GITHUB : testing team membership ..."

	activate_venv
	python $ESDOC_DIR_BASH/gh/test_team_membership.py --team=$1 --user=$2

	log "GITHUB : institutional teams initialized"
}

# Invoke entry point.
main $1 $2
