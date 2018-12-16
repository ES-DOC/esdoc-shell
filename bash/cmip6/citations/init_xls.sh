#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "CMIP6 citation XLS initialization: BEGINS ..."

	if [ "$1" ]; then
		institution=$1
	else
		institution=all
	fi
	xls_template=$ESDOC_DIR_BASH/cmip6/citations/templates/citations.xlsx

	activate_venv
	python $ESDOC_DIR_BASH/cmip6/citations/init_xls.py --institution-id=$institution --xls-template=$xls_template

    log "CMIP6 citation XLS initialization: ENDS ..."
}

# Invoke entry point.
main $1
