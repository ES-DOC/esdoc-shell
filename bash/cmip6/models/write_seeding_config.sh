#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	declare output_dir=$ESDOC_HOME/repos/esdoc-docs/cmip6/models/seeding
	python $ESDOC_HOME/bash/cmip6/models/write_seeding_config.py --output=$output_dir
	log "WCRP cmip6 model seeding config files written to "$output_dir
}

# Invoke entry point.
main