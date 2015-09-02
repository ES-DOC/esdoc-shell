#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	activate_venv api
	supervisorctl -c $ESDOC_DIR_DAEMONS/api/supervisord.conf stop all
	supervisorctl -c $ESDOC_DIR_DAEMONS/api/supervisord.conf shutdown
	log "WEB : killed daemons"
}

# Invoke entry point.
main
