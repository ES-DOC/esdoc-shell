#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "Initializing CMIP6 model output ..."

	activate_venv
	if [ $1 = "all" ]; then
		for institution_id in "${INSTITUTION_ID[@]}"
		do
			python $ESDOC_DIR_BASH/cmip6/models/init_output --institution-id=$institution_id
		done
		python $ESDOC_DIR_BASH/cmip6/models/init_output --institution-id=test-institute-1
		python $ESDOC_DIR_BASH/cmip6/models/init_output --institution-id=test-institute-2
		python $ESDOC_DIR_BASH/cmip6/models/init_output --institution-id=test-institute-3
	else
		python $ESDOC_DIR_BASH/cmip6/models/init_output --institution-id=$1
	fi

	log "CMIP6 model output Initialized ..."
}

# Invoke entry point.
main $1