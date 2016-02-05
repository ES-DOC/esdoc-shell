#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	python $ESDOC_HOME/bash/mp/write_cmip6_mindmap.py --dest=$ESDOC_DIR_REPOS/esdoc-cim/vocabs/cmip6/mindmaps --domain=$1
	cp $ESDOC_DIR_REPOS/esdoc-cim/vocabs/cmip6/mindmaps/* $ESDOC_DIR_REPOS/esdoc-docs/cmip6/mindmaps
}

# Invoke entry point.
main $1
