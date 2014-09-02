#!/bin/bash

# ###############################################################
# SECTION: DOCUMENT PROCESSING COMMANDS
# ###############################################################

run_doc_validate()
{
	activate_venv pyesdoc
	python $DIR_JOBS/pyesdoc/validate_document.py $1 $2
}