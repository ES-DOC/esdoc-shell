#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "PYESDOC : writing cmip6 model notebooks ..."

	declare input_dir=$ESDOC_DIR_REPOS
	declare output_dir=$ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/notebooks

	activate_venv pyesdoc
	python $ESDOC_HOME/bash/cmip6/write_model_notebooks.py --input=$input_dir --output=$output_dir

	log "PYESDOC : cmip6 model notebooks written to "$output_dir
}

# Invoke entry point.
main
