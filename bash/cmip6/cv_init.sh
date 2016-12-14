#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : writing WCRP cmip6 cv ..."

	declare source=$ESDOC_DIR_REPOS/cmip6-cv
	declare dest=$ESDOC_DIR_REPOS/esdoc-cv/wcrp

	activate_venv pyesdoc
	python $ESDOC_HOME/bash/cmip6/cv_init.py --source=$source --dest=$dest

	rm -rf $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/cv/archive/wcrp
	cp -r $dest $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/cv/archive/wcrp

	log "PYESDOC : WCRP cmip6 cv written to "$dest
	log "PYESDOC : WCRP cmip6 cv written to "$ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/cv/archive/wcrp
}

# Invoke entry point.
main
