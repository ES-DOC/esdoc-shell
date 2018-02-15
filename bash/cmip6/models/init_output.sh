#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "Initializing CMIP6 model output ..."

	activate_venv
	if [ $1 = "all" ]; then
		for institution_id in "${INSTITUTION_ID[@]}"
		do
			log "... initializing "$institution_id
			python $ESDOC_HOME/bash/cmip6/models/init_output --institution-id=$institution_id
		done
	else
		python $ESDOC_HOME/bash/cmip6/models/init_output --institution-id=$1
	fi

	log "CMIP6 model output Initialized ..."
}

# Invoke entry point.
main $1