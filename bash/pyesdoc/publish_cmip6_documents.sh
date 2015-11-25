#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : publishing cmip6 documents ..."
	activate_venv pyesdoc
	declare io_dir=$ESDOC_DIR_REPOS/esdoc-docs-cmip6/experiments/extracted
	declare spreadsheet=$ESDOC_DIR_REPOS/esdoc-docs-cmip6/experiments/cmip6-experiments-v2.xlsx
	rm -rf $io_dir/*.json
	rm -rf $io_dir/*.xml
	python $ESDOC_DIR_PYESDOC/jobs/run_publish_cmip6_documents.py --archive-dir=$io_dir --spreadsheet=$spreadsheet
	log "PYESDOC : cmip6 documents published to "$io_dir
}

# Invoke entry point.
main
