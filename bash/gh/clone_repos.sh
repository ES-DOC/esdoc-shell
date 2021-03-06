#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "GITHUB : cloning "$1" GitHub repos ..."

	activate_venv
	if [ $1 = "cmip6" ]; then
		source $ESDOC_DIR_BASH/gh/clone_repos_cmip6.sh
	fi

	log "GITHUB : cloned "$1" GitHub repos"
}

# Invoke entry point.
main $1
