#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : publishing cmip6 documents ..."
	# activate_venv pyesdoc
	python $ESDOC_DIR_PYESDOC/jobs/run_publish_cmip6_documents.py $1 $2
	log "PYESDOC : cmip6 documents published"
}

# Invoke entry point.
main $1 $2
