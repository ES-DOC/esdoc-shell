#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

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
		declare -a SPECIALIZATIONS=(
			'atmosphere'
			'ocean'
			'ocean-bgc'
			'seaice'
		)
		for specialization in "${SPECIALIZATIONS[@]}"
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
