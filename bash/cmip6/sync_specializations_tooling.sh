#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : syncing cmip6 specializations tooling ..."

	# Set of specializations.
	declare -a SPECIALIZATIONS=(
		'atmosphere'
		'seaice'
	)

	# Sync definitions.
	for specialization in "${SPECIALIZATIONS[@]}"
	do
		# ... remove previous
		rm -rf $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate
		mkdir $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate
		rm -rf $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/validate
		mkdir $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/validate
		# ... copy current
		cp $ESDOC_DIR_REPOS/cmip6-specializations-ocean/generate/* $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate
		cp $ESDOC_DIR_REPOS/cmip6-specializations-ocean/validate/* $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/validate
	done

	log "PYESDOC : syncing cmip6 specializations tooling"
}

# Invoke entry point.
main
