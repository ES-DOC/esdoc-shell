#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : validating document ..."
	activate_venv pyesdoc
	if [ "$2" ]; then
		python $ESDOC_DIR_PYESDOC/jobs/run_validate_document.py --file=$1 --outfile=$2
	else
		python $ESDOC_DIR_PYESDOC/jobs/run_validate_document.py --file=$1
	fi
}

# Invoke entry point.
main $1 $2
