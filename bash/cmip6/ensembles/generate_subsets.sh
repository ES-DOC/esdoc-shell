#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
function main()
{
	log "CMIP6 ensemble subsetting: BEGINS ..."

	if [ "$1" ]; then
		declare institution=$1
	else
		declare institution=all
	fi

    declare archive_dir=$ESDOC_DIR_REPOS_CORE/esdoc-cdf2cim-archive/data
	declare output_dir=$ESDOC_DIR_REPOS_CORE/esdoc-cdf2cim-archive/subset

	activate_venv
	python $ESDOC_DIR_BASH/cmip6/ensembles/generate_subsets.py --institution-id=$institution --archive-directory=$archive_dir --output-directory=$output_dir

	log "CMIP6 ensemble subsetting: END"
}

# Invoke entry point.
main $1
