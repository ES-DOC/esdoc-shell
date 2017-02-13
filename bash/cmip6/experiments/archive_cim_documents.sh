#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "PYESDOC : CMIP6 : archiving documents ..."

	declare source_dir=$ESDOC_DIR_REPOS/esdoc-docs/cmip6/experiments/cim-documents
	declare target_dir=$ESDOC_DIR_REPOS/esdoc-archive/esdoc/cmip6-draft/spreadsheet

	mkdir -p $target_dir
	rm -rf $target_dir/*.json

	activate_venv pyesdoc
	python $ESDOC_HOME/bash/cmip6/archive_documents.py --source-dir=$source_dir --target-dir=$target_dir

	log "PYESDOC : CMIP6 : archived documents @ "$target_dir
}

# Invoke entry point.
main
