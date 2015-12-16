#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_NB

	python $ESDOC_HOME/bash/nb/rewrite_cim2_schema.py --dest=$ESDOC_DIR_REPOS/esdoc-mp/esdoc_mp/schemas/cim/v2
}

# Invoke entry point.
main
