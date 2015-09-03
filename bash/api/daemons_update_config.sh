#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	cp $ESDOC_DIR_RESOURCES/template-webfaction-api-supervisord.conf $ESDOC_DIR_DAEMONS/api/supervisord.conf
	log "WEB : updated daemons config"
}

# Invoke entry point.
main
