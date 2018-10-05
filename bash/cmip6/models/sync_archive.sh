#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "CMIP6 ARCHIVE syncing model documents: BEGINS ..."

	archive_folder=$ESDOC_ARCHIVE_HOME/esdoc/cmip6/spreadsheet-models
	if [ "$1" ]; then
		rm -rf $archive_folder/cmip6_$1*.*
	else
		rm -rf $archive_folder/*.*
	fi

	activate_venv
	python $ESDOC_DIR_BASH/cmip6/models/sync_archive.py --archive-folder=$archive_folder --institution-id=$1

	log "CMIP6 ARCHIVE syncing model documents: END"
}

# Invoke entry point.
main $1