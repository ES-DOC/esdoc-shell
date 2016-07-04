#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : peeking at document ..."
	activate_venv pyesdoc

	if [ "$2" ]; then
		python $ESDOC_HOME/bash/pyesdoc/peek.py --file=$1 --encoding=$2
	else
		python $ESDOC_HOME/bash/pyesdoc/peek.py --file=$1
	fi
}

# Invoke entry point.
main $1 $2
