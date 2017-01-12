#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	cp $ESDOC_DIR_REPOS/esdoc-cim-v$1-schema/*.py $ESDOC_DIR_PYESDOC/pyesdoc/mp/ontologies/schemas/cim/v$1
	cp $ESDOC_DIR_REPOS/esdoc-cim-v$1-schema/*.py $ESDOC_DIR_REPOS/esdoc-cim/v$1/schema
}

# Invoke entry point.
main $1
