#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "INSTALLING INSTITUTIONAL REPOS"

	mkdir -p $ESDOC_DIR_REPOS_INSTITUTIONAL
	for institution in "${INSTITUTION_ID[@]}"
	do
		log "Installing institutional repo: $institution"
		# rm -rf $ESDOC_DIR_REPOS_INSTITUTIONAL/$institution
		# git clone -q https://github.com/ES-DOC-INSTITUTIONAL/$institution.git $ESDOC_DIR_REPOS_INSTITUTIONAL/$institution
	done

	log "INSTALLED INSTITUTIONAL REPOS"
}

# Invoke entry point.
main
