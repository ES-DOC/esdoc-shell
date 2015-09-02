#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	ps -ef | grep esdoc/shells
}

# Invoke entry point.
main
