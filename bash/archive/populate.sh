#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "populating archive ..."

	if [ "$1" ]; then
		declare throttle=$1
	else
		declare throttle=0
	fi
	if [ "$2" ]; then
		declare project=$2
	else
		declare project=""
	fi

	activate_venv pyesdoc
	python $ESDOC_DIR_PYESDOC/jobs/run_archive_populate.py --throttle=$throttle --project=$project

	log "populated archive ..."
}

# Invoke entry point.
main $1 $2