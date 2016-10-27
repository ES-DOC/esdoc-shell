#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	source $ESDOC_HOME/bash/mp/generate.sh cim 1 python
	source $ESDOC_HOME/bash/mp/generate.sh cim 1 qxml
}

# Invoke entry point.
main
