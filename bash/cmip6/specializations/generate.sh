#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Import vocab.
source $ESDOC_DIR_BASH/cmip6/specializations/vocab.sh

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
		for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
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
