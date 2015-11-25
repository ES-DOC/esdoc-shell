#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : writing cmip6 documents to archive ..."
	declare source_dir=$ESDOC_DIR_REPOS/esdoc-docs-cmip6/experiments/extracted
	declare target_dir=$ESDOC_DIR_REPOS/esdoc-archive/esdoc/cmip6-draft/spreadsheet
	mkdir -p $target_dir
	rm -rf $target_dir/*.json
	activate_venv pyesdoc
	python $ESDOC_DIR_PYESDOC/jobs/run_archive_cmip6_documents.py --source-dir=$source_dir --target-dir=$target_dir
	log "PYESDOC : cmip6 documents written to archive: "$target_dir
}

# Invoke entry point.
main
