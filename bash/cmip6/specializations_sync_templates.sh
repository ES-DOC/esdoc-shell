#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : syncing cmip6 specializations templates ..."

	# Set of specializations.
	declare -a SPECIALIZATIONS=(
		'aerosols'
		'atmosphere'
		'atmospheric-chemistry'
		'landice'
		'landsurface'
		'ocean-bgc'
		'seaice'
		'toplevel'
	)

	# Sync definitions.
	for specialization in "${SPECIALIZATIONS[@]}"
	do
		# ... remove previous
		rm -rf $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/templates
		mkdir $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/templates
		# ... copy current
		cp $ESDOC_DIR_REPOS/cmip6-specializations-ocean/templates/* $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/templates
	done

	log "PYESDOC : syncing cmip6 specializations templates"
}

# Invoke entry point.
main
