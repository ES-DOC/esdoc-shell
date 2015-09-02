#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	rm $ESDOC_DIR_LOGS/api/*.log
	rm $ESDOC_DIR_DAEMONS/api/supervisor.log
	log "WEB : reset daemon logs"
}

# Invoke entry point.
main
