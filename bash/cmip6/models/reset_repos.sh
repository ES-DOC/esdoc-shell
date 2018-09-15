#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	activate_venv
	for institution_id in "${INSTITUTION_ID[@]}"
	do
		echo $ESDOC_HOME/repos/institutional/$institution_id/cmip6/models
	done
}

# Invoke entry point.
main $1