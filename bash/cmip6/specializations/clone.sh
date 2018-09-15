#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Import vocab.
source $ESDOC_DIR_BASH/cmip6/specializations/vocab.sh

# Main entry point.
main()
{
	mkdir -p $ESDOC_DIR_CMIP6
	cd $ESDOC_DIR_CMIP6

	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		log "CMIP6-SPECS : cloning "$specialization
		git clone https://github.com/ES-DOC/cmip6-specializations-$specialization.git
	done
}

# Invoke entry point.
main
