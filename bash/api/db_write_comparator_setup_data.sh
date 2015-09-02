#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API : setting up comparator setup data ..."
	activate_venv api
	python $ESDOC_DIR_API/jobs/run_write_comparator_setup.py --outdir=$ESDOC_DIR_WEB_STATIC/data
	cp $ESDOC_DIR_WEB_STATIC/data/compare.setup*.* $ESDOC_DIR_WEB_COMPARATOR/src/data
    log "API : comparator setup data written ---> "$ESDOC_DIR_WEB_STATIC/data
    log "API : comparator setup data written ---> "$ESDOC_DIR_WEB_COMPARATOR/src/data
}

# Invoke entry point.
main
