#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "PYESDOC : writing cmip6 conformance config ..."

	declare input_dir=$ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/experiments/cim-documents
	declare output_dir=$ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/conformances/config

	rm -rf $output_dir/*.json

	activate_venv
	python $ESDOC_DIR_BASH/cmip6/conformances/write_config.py --input=$input_dir --output=$output_dir

	log "PYESDOC : cmip6 conformance config written to "$output_dir
}

# Invoke entry point.
main
