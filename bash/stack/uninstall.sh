#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "UNINSTALLING STACK"
	rm -rf $ESDOC_HOME
	log "UNINSTALLED STACK"
}

# Invoke entry point.
main
