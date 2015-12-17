#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_REPOS/esdoc-cv/cmip6/definitions

	rm $ESDOC_DIR_REPOS/esdoc-cv/cmip6/mindmaps/*.xmind

	python $ESDOC_HOME/bash/mp/write_cmip6_xmind.py --dest=$ESDOC_DIR_REPOS/esdoc-cv/cmip6/mindmaps
}

# Invoke entry point.
main
