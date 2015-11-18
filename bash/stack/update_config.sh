#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	cp $ESDOC_DIR_CONFIG/api.conf $ESDOC_DIR_CONFIG/api.conf-backup
	cp $ESDOC_DIR_CONFIG/pyesdoc.conf $ESDOC_DIR_CONFIG/pyesdoc.conf-backup
	cp $ESDOC_DIR_RESOURCES/template-user-api.conf $ESDOC_DIR_CONFIG/api.conf
	cp $ESDOC_DIR_RESOURCES/template-user-pyesdoc.conf $ESDOC_DIR_CONFIG/pyesdoc.conf
	log "UPDATED CONFIG"
	log "The update process created new config files:" 1
	log "$ESDOC_DIR_CONFIG/api.conf" 2
	log "$ESDOC_DIR_CONFIG/pyesdoc.conf" 2
	log "It also created a backup of your old config files:" 1
	log "$ESDOC_DIR_CONFIG/api.conf-backup" 2
	log "$ESDOC_DIR_CONFIG/pyesdoc.conf-backup" 2
	log "Please verify your local configuration settings accordingly." 1
}

# Invoke entry point.
main