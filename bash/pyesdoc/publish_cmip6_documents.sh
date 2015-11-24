#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : publishing cmip6 documents ..."
	# activate_venv pyesdoc
	log $1
	rm -rf $1/*.json
	rm -rf $1/*.xml
	python $ESDOC_DIR_PYESDOC/jobs/run_publish_cmip6_documents.py --archive-dir=$1 --spreadsheet=$2
	log "PYESDOC : cmip6 documents published"
}

# Invoke entry point.
main $1 $2
