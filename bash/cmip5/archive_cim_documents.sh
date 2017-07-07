#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "PYESDOC : CMIP5 : archiving documents ..."

	declare source_dir=$1
	declare target_dir=$ESDOC_DIR_REPOS/esdoc-archive/esdoc/cmip5/metafor-q

	activate_venv
	python $ESDOC_HOME/bash/cmip5/archive_cim_documents.py --source-dir=$source_dir --target-dir=$target_dir

	log "PYESDOC : CMIP5 : archived documents @ "$target_dir
}

# Invoke entry point.
main $1
