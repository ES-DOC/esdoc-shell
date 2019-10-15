#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "CMIP6 institute verification: BEGINS ..."

	activate_venv
	python $ESDOC_DIR_BASH/cmip6/institutes/verify_repos.py

	log "CMIP6 institute verification: END"
}

# Invoke entry point.
main