#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "initializing CMIP6 jupyterhub output archive ..."

	rm $ESDOC_HOME/bash/cmip6/jhub/init_archive/output.txt
	activate_venv
	python $ESDOC_HOME/bash/cmip6/jhub/init_archive
	cp $ESDOC_HOME/bash/cmip6/jhub/init_archive/output.txt $ESDOC_HOME/repos/esdoc-jupyterhub-archive/sh/init.sh

	log "CMIP6 jupyterhub output archive initialized"
}

# Invoke entry point.
main
