#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "GITHUB : cloning institutional repos ..."

	activate_venv

	mkdir $ESDOC_HOME/repos/institutional
	cd $ESDOC_HOME/repos/institutional

	for institution_id in "${INSTITUTION_ID[@]}"
	do
		git clone https://github.com/ES-DOC-INSTITUTIONAL/$institution_id.git
	done

	log "GITHUB : institutional repos cloned"
}

# Invoke entry point.
main
