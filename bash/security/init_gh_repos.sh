#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "CMIP6 : initializing CMIP6 institutional repos ..."

	activate_venv
	python $ESDOC_HOME/bash/cmip6/misc/init_gh_repos.py

	log "CMIP6 : CMIP6 institutional repos initialized"
}

# Invoke entry point.
main
