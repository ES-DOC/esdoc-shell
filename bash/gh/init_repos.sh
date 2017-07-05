#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "GITHUB : initializing institutional repos ..."

	activate_venv
	python $ESDOC_HOME/bash/gh/init_repos.py

	log "GITHUB : institutional repos initialized"
}

# Invoke entry point.
main
