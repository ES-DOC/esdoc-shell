#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "GITHUB : initializing institutional repos ..."

	activate_venv
	python $ESDOC_DIR_BASH/gh/init_repos.py

	log "GITHUB : institutional repos initialized"
}

# Invoke entry point.
main
