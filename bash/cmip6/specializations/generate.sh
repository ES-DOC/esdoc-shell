#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Array of active specifications.
declare -a _ACTIVE_SPECIALIZATIONS=(
	'atmos'
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
	if [ "$1" ]; then
		declare specialization=$1
		log_banner
		log "CMIP6-SPECS : generating "$specialization
		log_banner
		python $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/generate
	else
		for specialization in "${_ACTIVE_SPECIALIZATIONS[@]}"
		do
			log_banner
			log "CMIP6-SPECS : generating "$specialization
			log_banner
			python $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/generate
		done
	fi
}

# Invoke entry point.
main $1
