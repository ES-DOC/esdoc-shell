#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	source $ESDOC_HOME/bash/pyesdoc/mp_generate.sh cim 2 python
	source $ESDOC_HOME/bash/pyesdoc/mp_generate.sh cim 2 qconfig
}

# Invoke entry point.
main
