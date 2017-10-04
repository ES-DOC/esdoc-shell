#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "PYESDOC : mapping cmip5 model documents ..."

	activate_venv
	declare seeding_dir=$ESDOC_HOME/repos/esdoc-docs/cmip6/models/seeding
	python $ESDOC_HOME/bash/cmip6/models/write_from_cmip5 --encoding=$1 --output=$2 --seeding=$seeding_dir

	log "PYESDOC : cmip5 model documents mapped"
}

# Invoke entry point.
main $1 $2
