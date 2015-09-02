#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	source $ESDOC_HOME/bash/api/daemons_reset_logs.sh
	activate_venv api
	supervisord -c $ESDOC_DIR_DAEMONS/api/supervisord.conf
	log "WEB : initialized daemons"
}

# Invoke entry point.
main
