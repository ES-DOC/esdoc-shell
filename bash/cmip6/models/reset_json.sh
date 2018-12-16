#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "CMIP6 model JSON reset: BEGINS ..."

	if [ "$1" ]; then
		institution=$1
	else
		institution=all
	fi

	activate_venv
	python $ESDOC_DIR_BASH/cmip6/models/reset_json.py --institution-id=$institution

	log "CMIP6 model JSON reset: COMPLETE"
}

# Invoke entry point.
main $1
