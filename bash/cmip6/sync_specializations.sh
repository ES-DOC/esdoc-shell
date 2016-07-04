#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : syncing cmip6 specializations ..."

	# Set of specializations.
	declare -a CMIP6_SPECIALIZATIONS=(
		'ocean'
	)

	# Remove existing.
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		rm $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/definitions/$specialization*.py
		rm $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/mindmaps/$specialization.mm
		rm $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/config/$specialization.json
		rm $ESDOC_DIR_REPOS/esdoc-mp/esdoc_mp/specializations/cmip6/$specialization*.py
	done

	# Generate new.
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=mm
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=json
	done

	# Copy most recent.
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/$specialization*.py $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/definitions
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/$specialization*.py $ESDOC_DIR_REPOS/esdoc-mp/esdoc_mp/specializations/cmip6
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization.mm $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/mindmaps/$specialization.mm
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization.json $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/config/$specialization.json
	done

	log "PYESDOC : syncing cmip6 specializations"
}

# Invoke entry point.
main
