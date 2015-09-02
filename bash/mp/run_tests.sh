#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "MP : running tests ..."
	activate_venv mp
    nosetests -v -s $ESDOC_DIR_MP_TESTS
}

# Invoke entry point.
main
