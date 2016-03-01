#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_NB

	declare dest=$ESDOC_DIR_REPOS/esdoc-mp/esdoc_mp/ontologies/schemas/cim/v2

	python $ESDOC_HOME/bash/nb/rewrite_cim2_ontology.py --dest=$dest
}

# Invoke entry point.
main
