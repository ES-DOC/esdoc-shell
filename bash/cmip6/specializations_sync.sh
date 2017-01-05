#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : syncing cmip6 specializations ..."

	# Set of specializations.
	declare -a SPECIALIZATIONS=(
		'atmosphere'
		'ocean'
		'seaice'
	)

	# Update pyesdoc.
	for specialization in "${SPECIALIZATIONS[@]}"
	do
		rm $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations/cmip6/$specialization*.py
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/$specialization*.py $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations/cmip6
	done

	# Update generated artefacts.
	for specialization in "${SPECIALIZATIONS[@]}"
	do
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=mm
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=json
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=ids-level-1
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=ids-level-2
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=ids-level-3
	done

	# Updated esdoc-docs.
	for specialization in "${SPECIALIZATIONS[@]}"
	do
		# ... remove previously generated
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/config/$specialization.json
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization*.csv
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/mindmaps/$specialization.mm
		# ... copy generated
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization.mm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/mindmaps/$specialization.mm
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization.json $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/config/$specialization.json
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization-ids-level-1.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-1.csv
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization-ids-level-2.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-2.csv
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization-ids-level-3.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-3.csv
	done

	log "PYESDOC : syncing cmip6 specializations"
}

# Invoke entry point.
main
