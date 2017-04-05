#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "PYESDOC : writing cmip6 conformance spreadsheets ..."

	declare input_dir=$ESDOC_DIR_REPOS/esdoc-docs/cmip6/experiments/cim-documents
	declare output_dir=$ESDOC_DIR_REPOS/esdoc-docs/cmip6/conformances/spreadsheets

	rm -rf $output_dir/*.*

	activate_venv
	python $ESDOC_HOME/bash/cmip6/conformances/write_spreadsheets.py --input=$input_dir --output=$output_dir

	log "PYESDOC : cmip6 conformance spreadsheets written to "$output_dir
}

# Invoke entry point.
main
