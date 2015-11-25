#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : writing cmip6 documents ..."
	declare io_dir=$ESDOC_DIR_REPOS/esdoc-docs-cmip6/experiments/extracted
	declare spreadsheet=$ESDOC_DIR_REPOS/esdoc-docs-cmip6/experiments/cmip6-experiments-v2.xlsx
	rm -rf $io_dir/*.json
	rm -rf $io_dir/*.xml
	activate_venv pyesdoc
	python $ESDOC_DIR_PYESDOC/jobs/run_write_cmip6_documents.py --archive-dir=$io_dir --spreadsheet=$spreadsheet
	log "PYESDOC : cmip6 documents written to "$io_dir
}

# Invoke entry point.
main
