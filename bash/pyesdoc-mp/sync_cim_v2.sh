#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	source $ESDOC_HOME/bash/pyesdoc-mp/sync.sh 2
}

# Invoke entry point.
main