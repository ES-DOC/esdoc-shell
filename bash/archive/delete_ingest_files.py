#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "deleting ingest files from archive ..."
	activate_venv pyesdoc
	python $ESDOC_DIR_PYESDOC/jobs/run_archive_delete_ingest_files.py
    log "deleted ingest files from archive"

}

# Invoke entry point.
main $1 $2