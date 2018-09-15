#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Import vocab.
source $ESDOC_DIR_BASH/cmip6/specializations/vocab.sh

# Main entry point.
main()
{
	log "CMIP6-SPECS : syncing definitions ..."

	log "CMIP6-SPECS : syncing py files ..."
	rm $ESDOC_DIR_REPOS_CORE/esdoc-py-client/pyesdoc/mp/specializations/cmip6/*.py
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/$specialization*.py $ESDOC_DIR_REPOS_CORE/esdoc-py-client/pyesdoc/mp/specializations/cmip6
	done

	log "CMIP6-SPECS : syncing csv files ..."
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		rm $ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/models/csv/$specialization-ids-level-1.csv
		rm $ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/models/csv/$specialization-ids-level-2.csv
		rm $ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/models/csv/$specialization-ids-level-3.csv
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization-ids-level-1.csv $ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/models/csv/$specialization-ids-level-1.csv
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization-ids-level-2.csv $ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/models/csv/$specialization-ids-level-2.csv
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization-ids-level-3.csv $ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/models/csv/$specialization-ids-level-3.csv
	done

	log "CMIP6-SPECS : syncing json files ..."
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		rm $ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/models/config/$specialization.json
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization.json $ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/models/config/$specialization.json
	done

	log "CMIP6-SPECS : syncing mindmap files ..."
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		rm $ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/models/mindmaps/$specialization.mm
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization.mm $ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/models/mindmaps/$specialization.mm
	done

	log "CMIP6-SPECS : syncing cmip5 mapping files ..."
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		if [ $specialization != "toplevel" ]; then
			rm $ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/models/cmip5-mappings/$specialization-*.csv
			cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/mappings/*.csv $ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/models/cmip5-mappings
		fi
	done

	log "CMIP6-SPECS : synced definitions"
}

# Invoke entry point.
main
