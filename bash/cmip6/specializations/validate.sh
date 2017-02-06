#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	if [ "$1" ]; then
		declare specialization=$1
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/validate
	else
		declare -a SPECIALIZATIONS=(
			'atmosphere'
			'ocean'
			'oceanbgc'
			'seaice'
		)
		for specialization in "${SPECIALIZATIONS[@]}"
		do
			log "PYESDOC : validating "$specialization" artefacts ..."
			python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/validate
		done
	fi
}

# Invoke entry point.
main $1
