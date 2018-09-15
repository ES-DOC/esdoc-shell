#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Import vocab.
source $ESDOC_DIR_BASH/cmip6/specializations/vocab.sh

# Main entry point.
main()
{
	log "CMIP6-SPECS : syncing templates ..."

	for specialization in "${CMIP6_REALM_SPECIALIZATIONS[@]}"
	do
		rm -rf $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/templates
		mkdir $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/templates
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-toplevel/templates/* $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/templates
	done
}

# Invoke entry point.
main
