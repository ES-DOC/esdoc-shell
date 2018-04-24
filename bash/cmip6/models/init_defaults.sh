#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "CMIP6 model defaults initialisation begins ..."

	activate_venv
	if [ $1 = "all" ]; then
		for institution_id in "${INSTITUTION_ID[@]}"
		do
			python $ESDOC_HOME/bash/cmip6/models/init_defaults.py --institution-id=$institution_id
		done
	else
		python $ESDOC_HOME/bash/cmip6/models/init_defaults.py --institution-id=$1
	fi

	log "CMIP6 model defaults initialized ..."
}

# Invoke entry point.
main $1