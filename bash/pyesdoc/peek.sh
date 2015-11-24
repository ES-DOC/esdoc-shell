#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : peeking at document ..."
	activate_venv pyesdoc
	python $ESDOC_DIR_PYESDOC/jobs/run_peek_document.py --file=$1
}

# Invoke entry point.
main $1
