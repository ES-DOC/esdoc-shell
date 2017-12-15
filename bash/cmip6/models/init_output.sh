#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "CMIP6 model notebook output initialisation begins ..."

	activate_venv
	python $ESDOC_HOME/bash/cmip6/models/init_output

	log "CMIP6 model notebook output initialized ..."
}

# Invoke entry point.
main
