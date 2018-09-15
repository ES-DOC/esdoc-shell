#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "PYESDOC : CMIP5 : archiving documents ..."

	declare source_dir=$1
	declare target_dir=$ESDOC_DIR_REPOS_CORE/esdoc-archive/esdoc/cmip5/metafor-q

	activate_venv
	python $ESDOC_DIR_BASH/cmip5/archive_cim_documents.py --source-dir=$source_dir --target-dir=$target_dir

	log "PYESDOC : CMIP5 : archived documents @ "$target_dir
}

# Invoke entry point.
main $1
