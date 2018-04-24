#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Import vocab.
source $ESDOC_HOME/bash/cmip6/specializations/vocab.sh

# Main entry point.
main()
{
	log "CMIP6-SPECS : syncing mappings ..."

	rm -rf $ESDOC_HOME/bash/cmip6/models/init_output/csv-files/*.csv
	for specialization in "${CMIP6_REALM_SPECIALIZATIONS[@]}"
	do
		cp $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/mappings/*.csv $ESDOC_HOME/bash/cmip6/models/init_output/csv-files
	done

	log "CMIP6-SPECS : synced mappings"
}

# Invoke entry point.
main
