#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "GITHUB : writing CMIP6 model default spreadsheets ..."

	declare TEMPLATE=$ESDOC_HOME/repos/esdoc-docs/cmip6/models/spreadsheet/model-defaults.xlsx
	declare DEST=$ESDOC_HOME/repos/institutional

	for institution_id in "${INSTITUTION_ID[@]}"
	do
		mkdir -p $DEST/$institution_id/cmip6/models
		cp $TEMPLATE $DEST/$institution_id/cmip6/models
	done

	log "GITHUB : CMIP6 model default spreadsheets written ..."
}

# Invoke entry point.
main
