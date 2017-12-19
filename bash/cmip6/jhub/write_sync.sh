#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "CMIP6 model notebook syncing script begins ..."

	rm $ESDOC_HOME/bash/cmip6/jhub/write_sync/output.txt
	activate_venv
	python $ESDOC_HOME/bash/cmip6/jhub/write_sync
	cp $ESDOC_HOME/bash/cmip6/jhub/write_sync/output.txt $ESDOC_HOME/repos/esdoc-jupyterhub-archive/sh/sync_from_server.sh

	log "CMIP6 model notebook syncing script written"
}

# Invoke entry point.
main
