#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	source $ESDOC_HOME/bash/pyesdoc/mp_validate.sh cim 1
}

# Invoke entry point.
main
