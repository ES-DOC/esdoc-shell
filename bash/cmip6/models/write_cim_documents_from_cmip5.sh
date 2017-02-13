#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "PYESDOC : converting cmip5 model documents ..."

	declare output_dir=$ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/from-cmip5
	activate_venv pyesdoc
	python $ESDOC_HOME/bash/cmip6/models/write_cim_documents_from_cmip5 --output=$output_dir

	log "PYESDOC : cmip5 model documents written to "$output_dir
}

# Invoke entry point.
main
