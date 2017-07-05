#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Array of active specifications.
declare -a _ACTIVE_SPECIALIZATIONS=(
	'toplevel'
	'atmos'
	'land'
	'landice'
	'ocean'
	'ocnbgchem'
	'seaice'
)

# Main entry point.
main()
{
	if [ "$1" ]; then
		declare specialization=$1
		python $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/validate
	else
		for specialization in "${_ACTIVE_SPECIALIZATIONS[@]}"
		do
			python $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/validate
		done
	fi
}

# Invoke entry point.
main $1
