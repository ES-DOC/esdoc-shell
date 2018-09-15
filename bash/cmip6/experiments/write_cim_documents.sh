#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "PYESDOC : writing cmip6 experiments ..."

	declare io_dir=$ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/experiments/cim-documents
	declare spreadsheet=$ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/experiments/spreadsheet/experiments.xlsx
	declare identifiers=$ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/experiments/spreadsheet/document-identifiers.txt

	rm -rf $io_dir/*.json
	rm -rf $io_dir/*.xml

	activate_venv
	python $ESDOC_DIR_BASH/cmip6/experiments/write_cim_documents --io-dir=$io_dir --spreadsheet=$spreadsheet --identifiers=$identifiers

	log "PYESDOC : cmip6 experiments written to "$io_dir
}

# Invoke entry point.
main
