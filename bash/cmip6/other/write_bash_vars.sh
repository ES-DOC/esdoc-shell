#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	python $ESDOC_DIR_BASH/cmip6/other/write_bash_vars.py
	cp $ESDOC_DIR_BASH/cmip6/other/write_bash_vars_output.sh $ESDOC_DIR_BASH/utils_vocabs.sh
	log "WCRP cmip6 vocabs bash file written to "$ESDOC_DIR_BASH/utils_vocabs.sh
}

# Invoke entry point.
main