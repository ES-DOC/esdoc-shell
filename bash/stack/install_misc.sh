#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "INSTALLING MISC REPOS"

	mkdir -p $ESDOC_DIR_REPOS_MISC
	for repo in "${INSTITUTION_ID[@]}"
	do
		log "Installing miscellaneous repo: $repo"
		# rm -rf $ESDOC_DIR_REPOS_MISC/$repo
		# git clone -q https://github.com/ES-DOC-INSTITUTIONAL/$institution.git $ESDOC_DIR_REPOS_INSTITUTIONAL/$institution
	done

	log "INSTALLED MISC REPOS"
}

# Invoke entry point.
main
