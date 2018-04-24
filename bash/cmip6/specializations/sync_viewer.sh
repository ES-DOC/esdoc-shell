#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Import vocab.
source $ESDOC_HOME/bash/cmip6/specializations/vocab.sh

# Main entry point.
main()
{
	log "CMIP6-SPECS : syncing viewer data files ..."

	# Sync data files.
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		cp -r $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization.js $ESDOC_DIR_REPOS/esdoc-web-view-specialization/data/cmip6_$specialization.js
	done

	log "CMIP6-SPECS : synced viewer data files "
}

# Invoke entry point.
main
