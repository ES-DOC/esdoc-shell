#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API : running tests ..."
	activate_venv api
    nosetests -v -s $ESDOC_DIR_API_TESTS
}

# Invoke entry point.
main
