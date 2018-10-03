#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "CMIP5 documents initialization: START ..."

	activate_venv
	python $ESDOC_DIR_BASH/cmip6/models/init_cmip5_docs.py

	log "CMIP5 documents initialization: END"
}

# Invoke entry point.
main