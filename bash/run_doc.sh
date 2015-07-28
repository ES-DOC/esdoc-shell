#!/bin/bash

# ###############################################################
# SECTION: DOCUMENT PROCESSING COMMANDS
# ###############################################################

run_doc_validate()
{
	activate_venv pyesdoc

	if [ "$2" ]; then
		python $DIR_PYESDOC/jobs/run_validate_document.py --file=$1 --outfile=$2
	else
		python $DIR_PYESDOC/jobs/run_validate_document.py --file=$1
	fi
}

run_doc_convert()
{
	activate_venv pyesdoc

	python $DIR_PYESDOC/jobs/run_convert_document.py --file=$1 --encoding=$2
}
