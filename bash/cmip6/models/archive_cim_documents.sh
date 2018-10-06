#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "CMIP6 ARCHIVE model documents: BEGINS ..."

	archive_folder=$ESDOC_ARCHIVE_HOME/esdoc/cmip6/spreadsheet-models
	if [ "$1" ]; then
		rm -rf $archive_folder/cmip6_$1*.*
	else
		rm -rf $archive_folder/*.*
	fi

	activate_venv
	python $ESDOC_DIR_BASH/cmip6/models/archive_cim_documents.py --destination=$archive_folder --institution-id=$1

	log "CMIP6 ARCHIVE model documents: END"
}

# Invoke entry point.
main $1