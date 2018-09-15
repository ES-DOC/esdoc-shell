#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "GITHUB : pushing institutional GitHub repo changes ..."

	for institution_id in "${INSTITUTION_ID[@]}"
	do
		cd $ESDOC_HOME/repos/institutional/$institution_id
		git add *
		git commit -m $1
		git push origin master
	done

	cd $ESDOC_HOME/repos/institutional/test-institute-1
	git add *
	git commit -m $1
	git push origin master

	cd $ESDOC_HOME/repos/institutional/test-institute-2
	git add *
	git commit -m $1
	git push origin master

	cd $ESDOC_HOME/repos/institutional/test-institute-3
	git add *
	git commit -m $1
	git push origin master

	log "GITHUB : institutional GitHub repo changes pushed..."
}

# Invoke entry point.
main $1
