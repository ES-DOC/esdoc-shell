#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : syncing cmip6 specializations ..."

	# Set of specializations.
	declare -a SPECIALIZATIONS=(
		'ocean'
	)

	# Sync definitions.
	for specialization in "${SPECIALIZATIONS[@]}"
	do
		# ... remove previous
		rm $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/definitions/$specialization*.py
		rm $ESDOC_DIR_REPOS/esdoc-mp/esdoc_mp/specializations/cmip6/$specialization*.py
		# ... copy current
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/$specialization*.py $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/definitions
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/$specialization*.py $ESDOC_DIR_REPOS/esdoc-mp/esdoc_mp/specializations/cmip6
	done

	# Sync generated.
	for specialization in "${SPECIALIZATIONS[@]}"
	do
		# ... remove previous
		rm $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/mindmaps/$specialization.mm
		rm $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/config/$specialization.json
		rm $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/csv/$specialization*.csv
		# ... regenerate
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=mm
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=json
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=ids-level-1
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=ids-level-2
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=ids-level-3
		# ... copy generated
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization-ids-level-1.csv $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/csv/$specialization-ids-level-1.csv
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization-ids-level-2.csv $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/csv/$specialization-ids-level-2.csv
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization-ids-level-3.csv $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/csv/$specialization-ids-level-3.csv
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization.mm $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/mindmaps/$specialization.mm
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization.json $ESDOC_DIR_REPOS/esdoc-cim/v2/specializations/cmip6/config/$specialization.json
	done

	log "PYESDOC : syncing cmip6 specializations"
}

# Invoke entry point.
main
