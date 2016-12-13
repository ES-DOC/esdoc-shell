#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : writing cmip6 cv ..."

	declare source=$ESDOC_DIR_REPOS/cmip6-cv
	declare dest=$ESDOC_DIR_REPOS/esdoc-cv/wcrp

	activate_venv pyesdoc
	python $ESDOC_HOME/bash/cmip6/write_cv.py --source=$source --dest=$dest

	log "PYESDOC : cmip6 cv written to "$dest
}

# Invoke entry point.
main
