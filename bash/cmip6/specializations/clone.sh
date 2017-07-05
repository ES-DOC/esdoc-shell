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
	mkdir -p $ESDOC_DIR_CMIP6
	cd $ESDOC_DIR_CMIP6

	for specialization in "${_REALM_SPECIALIZATIONS[@]}"
	do
		log "CMIP6-SPECS : cloning "$specialization
		git clone https://github.com/ES-DOC/cmip6-specializations-$specialization.git
	done
}

# Invoke entry point.
main
