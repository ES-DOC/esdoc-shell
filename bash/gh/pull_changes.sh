#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "GITHUB : pulling institutional GitHub repo updates ..."

	for institution_id in "${INSTITUTION_ID[@]}"
	do
		log "GITHUB : pulling  "$institution_id
		cd $ESDOC_HOME/repos/institutional/$institution_id
		git pull
	done

	log "GITHUB : pulling test-institute-1"
	cd $ESDOC_HOME/repos/institutional/test-institute-1
	git pull

	log "GITHUB : pulling test-institute-2"
	cd $ESDOC_HOME/repos/institutional/test-institute-2
	git pull

	log "GITHUB : pulling test-institute-3"
	cd $ESDOC_HOME/repos/institutional/test-institute-3
	git pull

	log "GITHUB : institutional GitHub repo updates pulled"
}

# Invoke entry point.
main $1
