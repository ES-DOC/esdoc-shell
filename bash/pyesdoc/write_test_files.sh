#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : writing test files ..."
	activate_venv pyesdoc
	python $ESDOC_HOME/bash/pyesdoc/write_test_files.py --outdir=$ESDOC_DIR_PYESDOC_TESTS/files
	log "PYESDOC : test files written to "$ESDOC_DIR_PYESDOC_TESTS/files
}

# Invoke entry point.
main
