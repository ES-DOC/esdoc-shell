#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "GITHUB : aborting institutional repos ..."

	for institution_id in "${INSTITUTION_ID[@]}"
	do
		cd $ESDOC_HOME/repos/institutional/$institution_id
		git reset --hard
	done

	log "GITHUB : institutional repos aborted"
}

# Invoke entry point.
main
