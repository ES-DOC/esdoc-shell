#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	python $ESDOC_HOME/bash/cmip6/other/write_bash_vars.py
	cp $ESDOC_HOME/bash/cmip6/other/write_bash_vars_output.sh $ESDOC_HOME/bash/utils_vocabs.sh
	log "WCRP cmip6 vocabs bash file written to "$ESDOC_HOME/bash/utils_vocabs.sh
}

# Invoke entry point.
main