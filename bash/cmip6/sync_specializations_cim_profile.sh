#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : syncing cmip6 specializations CIM profile ..."

	cp $ESDOC_DIR_REPOS/cmip6-specializations-toplevel/cim_profile.py $ESDOC_DIR_REPOS/cmip6-specializations-ocean/generate/model/cim_profile.py

	log "PYESDOC : syncing cmip6 specializations CIM profile"
}

# Invoke entry point.
main
