#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : writing demo files ..."
	activate_venv pyesdoc
	python $ESDOC_HOME/bash/pyesdoc/write_demo_files.py --outdir=$ESDOC_DIR_WEB_VIEWER/media/html
	log "PYESDOC : demo files written to "$ESDOC_DIR_WEB_VIEWER/media/html
}

# Invoke entry point.
main
