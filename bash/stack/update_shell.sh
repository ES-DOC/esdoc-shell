#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "UPDATING SHELL"
	set_working_dir
	git pull -q
	remove_files "*.pyc"
	log "UPDATED SHELL"
}

# Invoke entry point.
main
