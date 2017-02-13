#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "PYESDOC : writing cmip6 model notebooks ..."

	declare output_dir=$ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/ipython
	activate_venv pyesdoc
	python $ESDOC_HOME/bash/cmip6/models/write_notebooks.py --output=$output_dir

	log "PYESDOC : cmip6 model notebooks written to "$output_dir/notebooks
}

# Invoke entry point.
main
