#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "GITHUB : pushing institutional GitHub repo changes ..."

	for institution_id in "${INSTITUTION_ID[@]}"
	do
		cd $ESDOC_HOME/repos/institutional/$institution_id
		git add *
		git commit -m "Model default spreadsheets"
		git push origin master
	done

	log "GITHUB : institutional GitHub repo changes pushed..."
}

# Invoke entry point.
main