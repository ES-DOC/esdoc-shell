#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : publishing to pypi ..."

	set_working_dir $ESDOC_DIR_PYESDOC
	python ./setup.py sdist upload

	log "PYESDOC : published to pypi ..."
}

# Invoke entry point.
main
