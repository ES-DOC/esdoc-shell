#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "PYESDOC : writing WCRP cmip6 cv ..."

	declare source=$ESDOC_DIR_REPOS/cmip6-cv
	declare dest=$ESDOC_DIR_REPOS/esdoc-cv/wcrp
	declare dest_pyesdoc=$ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/cv/archive/wcrp

	activate_venv pyesdoc
	python $ESDOC_HOME/bash/cmip6/cv/init.py --source=$source --dest=$dest

	rm -rf $dest_pyesdoc
	cp -r $dest $dest_pyesdoc

	log "PYESDOC : WCRP cmip6 cv written to "$dest
	log "PYESDOC : WCRP cmip6 cv written to "$dest_pyesdoc
}

# Invoke entry point.
main
