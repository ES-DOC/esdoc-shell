#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	cp $ESDOC_DIR_REPOS/esdoc-cim/v2/schema/*.py $ESDOC_DIR_REPOS/esdoc-mp/esdoc_mp/ontologies/schemas/cim/v2
	source $ESDOC_HOME/bash/mp/generate.sh cim 2 python
}

# Invoke entry point.
main
