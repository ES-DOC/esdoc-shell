#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Import vocab.
source $ESDOC_HOME/bash/cmip6/specializations/vocab.sh

# Main entry point.
main()
{
	log "CMIP6-SPECS : syncing viewer ..."

	# Sync js files.
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		cp -r $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/_$specialization.js $ESDOC_DIR_REPOS/esdoc-web-view-specialization/data/cmip6_$specialization.js
	done
	log "CMIP6-SPECS : synced js files"

	# Sync media.
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		rm -rf $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/media
		cp -r $ESDOC_DIR_REPOS/esdoc-web-view-specialization/media $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization
	done
	log "CMIP6-SPECS : synced media files"

}

# Invoke entry point.
main
