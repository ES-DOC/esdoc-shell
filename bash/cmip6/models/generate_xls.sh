#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "generating CMIP6 model XLS files ..."

	activate_venv
	if [ $1 = "all" ]; then
		for institution_id in "${INSTITUTION_ID[@]}"
		do
			python $ESDOC_DIR_BASH/cmip6/models/generate_xls.py --institution-id=$institution_id
		done
	else
		python $ESDOC_DIR_BASH/cmip6/models/generate_xls.py --institution-id=$1
	fi

	log "CMIP6 model XLS files generated ..."
}

# Invoke entry point.
main $1