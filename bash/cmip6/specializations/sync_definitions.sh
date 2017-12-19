#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Import vocab.
source $ESDOC_HOME/bash/cmip6/specializations/vocab.sh

# Main entry point.
main()
{
	log "CMIP6-SPECS : syncing definitions ..."

	log "CMIP6-SPECS : syncing py files ..."
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		rm $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations/cmip6/$specialization*.py
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/$specialization*.py $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations/cmip6
	done

	log "CMIP6-SPECS : syncing csv files ..."
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-1.csv
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-2.csv
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-3.csv
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization-ids-level-1.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-1.csv
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization-ids-level-2.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-2.csv
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization-ids-level-3.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-3.csv
	done

	log "CMIP6-SPECS : syncing json files ..."
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/config/$specialization.json
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization.json $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/config/$specialization.json
	done

	log "CMIP6-SPECS : syncing mindmap files ..."
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/mindmaps/$specialization.mm
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization.mm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/mindmaps/$specialization.mm
	done

	log "CMIP6-SPECS : syncing cmip5 mapping files ..."
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/cmip5-mappings/$specialization-cmip5-to-cmip6-mappings.csv
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/mappings/$specialization-cmip5-to-cmip6-mappings.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/cmip5-mappings/$specialization-cmip5-to-cmip6-mappings.csv
	done
}

# Invoke entry point.
main
