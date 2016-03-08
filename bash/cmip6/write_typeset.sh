#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "writing cmip6 typeset ..."

	# Set stylesheet & I/O destination.
	declare dest=$ESDOC_DIR_REPOS/esdoc-docs/cmip6/typeset

	# Invoke generator.
	activate_venv mp
	python $ESDOC_DIR_MP"/esdoc_mp/vocabs/cmip6/generators/typeset.py" --dest=$dest

	# Copy typeset to pyesdoc.
	# cp $ESDOC_DIR_REPOS/esdoc-cim/vocabs/cmip6/mindmaps/* $ESDOC_DIR_REPOS/esdoc-docs/cmip6/mindmaps

	log "written cmip6 typeset ..."
}

# Invoke entry point.
main $1 $2
