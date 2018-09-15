#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Import vocab.
source $ESDOC_DIR_BASH/cmip6/specializations/vocab.sh

# Main entry point.
main()
{
	log "CMIP6-SPECS : syncing cim profile ..."

	for specialization in "${CMIP6_REALM_SPECIALIZATIONS[@]}"
	do
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-toplevel/cim_profile.py $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/generate/cim_profile.py
	done
}

# Invoke entry point.
main
