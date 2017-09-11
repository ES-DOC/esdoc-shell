#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Import vocab.
source $ESDOC_HOME/bash/cmip6/specializations/vocab.sh

# Main entry point.
main()
{
	log "CMIP6-SPECS : syncing definitions ..."

	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		rm $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations/cmip6/$specialization*.py
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization*.csv
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/config/$specialization.json
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/mindmaps/$specialization.mm
	done

	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		log "CMIP6-SPECS : syncing py files ..."
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/$specialization*.py $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations/cmip6

		# log "CMIP6-SPECS : syncing csv files ..."
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization-ids-level-1.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-1.csv
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization-ids-level-2.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-2.csv
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization-ids-level-3.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-3.csv

		# log "CMIP6-SPECS : syncing json files ..."
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization.json $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/config/$specialization.json

		# log "CMIP6-SPECS : syncing mindmap files ..."
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization.mm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/mindmaps/$specialization.mm

	done
}

# Invoke entry point.
main
