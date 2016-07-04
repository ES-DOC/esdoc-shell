#!/bin/bash

# Activate shell (if necessary).
if [ ! "$ESDOC_HOME" ]; then
	source "$( dirname "$( dirname "$( dirname "${BASH_SOURCE[0]}" )" )" )"/activate
fi

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
	python $ESDOC_HOME/bash/archive/populate.py --throttle=$throttle --project=$project
    deactivate

	log "populated archive ..."
}

# Invoke entry point.
main $1 $2