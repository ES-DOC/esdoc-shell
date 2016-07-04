#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	activate_venv pyesdoc
	python $ESDOC_HOME/bash/archive/echo.py --uid=$1 --version=$2
}

# Invoke entry point.
main $1 $2