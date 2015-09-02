#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	activate_venv server
	supervisorctl -c $ESDOC_DIR_DAEMONS/api/supervisord.conf status all
}

# Invoke entry point.
main
