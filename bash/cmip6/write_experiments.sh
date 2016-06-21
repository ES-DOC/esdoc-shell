#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : writing cmip6 experiments ..."

	declare io_dir=$ESDOC_DIR_REPOS/esdoc-docs/cmip6/experiments/extracted
	declare spreadsheet=$ESDOC_DIR_REPOS/esdoc-docs/cmip6/experiments/cmip6-experiments-v33.xlsx
	declare identifiers=$ESDOC_DIR_REPOS/esdoc-docs/cmip6/experiments/cmip6-experiments-document-identifiers.txt

	rm -rf $io_dir/*.json
	rm -rf $io_dir/*.xml

	activate_venv pyesdoc
	python $ESDOC_DIR_PYESDOC/jobs/run_cmip6_write_experiments.py --io-dir=$io_dir --spreadsheet=$spreadsheet --identifiers=$identifiers

	log "PYESDOC : cmip6 experiments written to "$io_dir
}

# Invoke entry point.
main
