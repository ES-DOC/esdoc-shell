#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "generating CMIP6 model XLS files ..."

	activate_venv
	if [ $1 = "all" ]; then
		for institution_id in "${INSTITUTION_ID[@]}"
		do
			python $ESDOC_HOME/bash/cmip6/models/generate_xls.py --institution-id=$institution_id
		done
		python $ESDOC_HOME/bash/cmip6/models/generate_xls.py --institution-id=test-institute-1
		python $ESDOC_HOME/bash/cmip6/models/generate_xls.py --institution-id=test-institute-2
		python $ESDOC_HOME/bash/cmip6/models/generate_xls.py --institution-id=test-institute-3
	else
		python $ESDOC_HOME/bash/cmip6/models/generate_xls.py --institution-id=$1
	fi

	log "CMIP6 model XLS files generated ..."
}

# Invoke entry point.
main $1