#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	declare ontology=$1
	declare version=$2

	activate_venv mp

	echo "TODO: emit validation report: "$1" :: "$2
}

# Invoke entry point.
main $1 $2
