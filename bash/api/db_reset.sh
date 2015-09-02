#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "API-DB : resetting ..."
	source $ESDOC_DIR_BASH/api/db_uninstall.sh
	source $ESDOC_DIR_BASH/api/db_install.sh
	log "API-DB : reset"
}

# Invoke entry point.
main
