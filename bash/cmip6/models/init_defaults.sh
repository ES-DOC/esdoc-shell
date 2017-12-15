#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "CMIP6 model defaults initialisation begins ..."

	activate_venv
	python $ESDOC_HOME/bash/cmip6/models/init_defaults

	log "CMIP6 model defaults initialized ..."
}

# Invoke entry point.
main