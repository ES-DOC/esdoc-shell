#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "GITHUB : synching "$1" GitHub repos ..."

	activate_venv
	if [ $1 = "cmip6" ]; then
		python $ESDOC_DIR_BASH/gh/sync_repos_cmip6.py
	fi

	log "GITHUB : synched "$1" GitHub repos"
}

# Invoke entry point.
main $1
