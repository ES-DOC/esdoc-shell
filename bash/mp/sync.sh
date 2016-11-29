#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	cp $ESDOC_DIR_REPOS/esdoc-cim-v$1-schema/*.py $ESDOC_DIR_REPOS/esdoc-mp/esdoc_mp/ontologies/schemas/cim/v$1
	cp $ESDOC_DIR_REPOS/esdoc-cim-v$1-schema/*.py $ESDOC_DIR_REPOS/esdoc-cim/v$1/schema
}

# Invoke entry point.
main $1
