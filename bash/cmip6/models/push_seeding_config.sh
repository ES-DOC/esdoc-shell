#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "GITHUB : writing CMIP6 model seeding configuration ..."

	declare DEST=$ESDOC_HOME/repos/institutional

	for institution_id in "${INSTITUTION_ID[@]}"
	do
		mkdir -p $DEST/$institution_id/cmip6/models
		cp $ESDOC_HOME/repos/esdoc-docs/cmip6/models/seeding/$institution_id.json $DEST/$institution_id/cmip6/models/model-defaults.json
	done

	log "GITHUB : CMIP6 model seeding configuration written..."
}

# Invoke entry point.
main
