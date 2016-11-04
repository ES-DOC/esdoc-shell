#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "MP : publishing to pypi ..."

	set_working_dir $ESDOC_DIR_MP
	python ./setup.py sdist upload

	log "MP : published to pypi ..."
}

# Invoke entry point.
main
