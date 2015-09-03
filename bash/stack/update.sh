#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "UPDATING STACK"

	source $ESDOC_HOME/bash/stack/update_shell.sh
	source $ESDOC_HOME/bash/stack/update_config.sh
	source $ESDOC_HOME/bash/stack/update_repos.sh
	source $ESDOC_HOME/bash/stack/upgrade_venvs.sh

	log "UPDATED STACK"
}

# Invoke entry point.
main
