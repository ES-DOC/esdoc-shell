#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Import vocab.
source $ESDOC_DIR_BASH/cmip6/specializations/vocab.sh

# Main entry point.
main()
{
	cd $ESDOC_HOME/repos
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		log "CMIP6-SPECS : pulling "$specialization
		cd $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization
		git pull
	done
}

# Invoke entry point.
main
