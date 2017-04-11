#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Array of active specifications.
declare -a _ACTIVE_SPECIALIZATIONS=(
	'toplevel'
	'atmos'
	'land'
	'ocean'
	'ocnbgchem'
	'seaice'
)

# Main entry point.
main()
{
	if [ "$1" ]; then
		declare specialization=$1
		log_banner
		log "PYESDOC : generating "$specialization" artefacts"
		log_banner
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate
	else
		for specialization in "${_ACTIVE_SPECIALIZATIONS[@]}"
		do
			log_banner
			log "PYESDOC : generating "$specialization" artefacts"
			log_banner
			python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate
		done
	fi
}

# Invoke entry point.
main $1
