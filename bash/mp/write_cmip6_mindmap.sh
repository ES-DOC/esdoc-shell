#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "writing cmip6 mindmap(s) ..."

	# Set stylesheet & I/O destination.
	if [ "$2" ]; then
		declare stylesheet=$2
	else
		declare stylesheet=$ESDOC_DIR_BASH/mp/write_cmip6_mindmap.conf
	fi
	declare dest=$ESDOC_DIR_REPOS/esdoc-cim/vocabs/cmip6/mindmaps

	# Invoke mindmap generator.
	activate_venv mp
	python $ESDOC_DIR_MP"/esdoc_mp/vocabs/cmip6/mindmap.py" --dest=$dest --domain=$1 --stylesheet=$stylesheet

	# Copy mindmaps to esdoc-docs repo.
	cp $ESDOC_DIR_REPOS/esdoc-cim/vocabs/cmip6/mindmaps/* $ESDOC_DIR_REPOS/esdoc-docs/cmip6/mindmaps

	log "written cmip6 mindmap(s) ..."
}

# Invoke entry point.
main $1 $2
