#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "PYESDOC : writing cmip6 model notebooks ..."

	activate_venv
	export ESDOC_CMIP6_NOTEBOOK_HOME=$ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/ipython
	python $ESDOC_HOME/bash/cmip6/models/write_notebooks.py

	log "PYESDOC : cmip6 model notebooks written to "$ESDOC_CMIP6_NOTEBOOK_HOME
}

# Invoke entry point.
main
