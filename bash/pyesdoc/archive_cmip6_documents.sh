#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : archiving cmip6 documents ..."
	declare source_dir=$ESDOC_DIR_REPOS/esdoc-docs-cmip6/experiments/extracted
	declare target_dir=$ESDOC_DIR_REPOS/esdoc-archive/esdoc/cmip6-draft/spreadsheet
	rm -rf $target_dir/*.json
	activate_venv pyesdoc
	python $ESDOC_DIR_PYESDOC/jobs/run_archive_cmip6_documents.py --source-dir=$source_dir --target-dir=$target_dir
	log "PYESDOC : cmip6 documents archived to "$target_dir
}

# Invoke entry point.
main
