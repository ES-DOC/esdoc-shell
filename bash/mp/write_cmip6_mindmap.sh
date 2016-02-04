#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_REPOS/esdoc-cv/cmip6/definitions

	python $ESDOC_HOME/bash/mp/write_cmip6_mindmap.py --dest=$ESDOC_DIR_REPOS/esdoc-cv/cmip6/mindmaps --domain=$1
}

# Invoke entry point.
main $1
