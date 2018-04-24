#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

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