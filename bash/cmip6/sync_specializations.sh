#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : syncing cmip6 specializations ..."

	# Copy from satellite repos to esdoc-cim repo.
	cp $ESDOC_DIR_REPOS/cmip6-specializations-atmosphere/atmosphere*.py $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/definitions
	cp $ESDOC_DIR_REPOS/cmip6-specializations-ocean/ocean*.* $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/definitions
	cp $ESDOC_DIR_REPOS/cmip6-specializations-seaice/seaice*.* $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/definitions

	# Copy all to esdoc-mp repo.
	cp $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/definitions/*.py $ESDOC_DIR_REPOS/esdoc-mp/esdoc_mp/specializations/cmip6/schema

	log "PYESDOC : syncing cmip6 specializations"
}

# Invoke entry point.
main
