#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "CMIP6 PDF file generation: BEGINS ..."

	if [ "$1" ]; then
		institution=$1
	else
		institution=all
	fi

	activate_venv
	python $ESDOC_DIR_BASH/cmip6/models/generate_pdf.py --institution-id=$institution

	log "CMIP6 PDF file generation: END"
}

# Invoke entry point.
main $1