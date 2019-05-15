#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "PYESDOC : CMIP6 : archiving documents ..."

	declare source_dir=$ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/experiments/cim-documents
	declare target_dir=$ESDOC_DIR_REPOS_CORE/esdoc-archive/esdoc/cmip6/spreadsheet-experiments

	rm -rf $target_dir
	mkdir -p $target_dir

	activate_venv
	python $ESDOC_DIR_BASH/cmip6/experiments/archive_cim_documents.py --source-dir=$source_dir --target-dir=$target_dir

	log "PYESDOC : CMIP6 : archived documents @ "$target_dir
}

# Invoke entry point.
main
