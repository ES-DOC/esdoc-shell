#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Array of realm specifications.
declare -a _REALM_SPECIALIZATIONS=(
	'aerosol'
	'atmos'
	'atmoschem'
	'land'
	'landice'
	'ocean'
	'ocnbgchem'
	'seaice'
	'toplevel'
)

# Main entry point.
main()
{
	cd $ESDOC_HOME/repos
	for specialization in "${_REALM_SPECIALIZATIONS[@]}"
	do
		log "CMIP6-SPECS : pulling "$specialization
		cd $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization
		git pull
	done
}

# Invoke entry point.
main
