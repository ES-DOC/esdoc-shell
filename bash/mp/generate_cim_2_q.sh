#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	source $ESDOC_HOME/bash/mp/generate.sh cim 2 qxml
}

# Invoke entry point.
main
