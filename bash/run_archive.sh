#!/bin/bash

# ###############################################################
# SECTION: ARCHIVE FUNCTIONS
# ###############################################################


# Echos contents of an archived file.
run_archive_echo()
{
	activate_venv pyesdoc
	python $DIR_JOBS/archive/run_echo.py --uid=$1 --version=$2
}

# Deletes ingest files from the archive.
_run_archive_delete_ingest_files()
{
    log "deleting ingest files from archive ..."

	activate_venv pyesdoc
	python $DIR_JOBS/archive/run_delete_ingest_files.py

    log "deleted ingest files from archive ..."
}

# Pulls documents from remote sources into the archive.
run_archive_populate()
{
	log "populating archive ..."

	if [ "$1" ]; then
		declare throttle=$1
	else
		declare throttle=0
	fi
	if [ "$2" ]; then
		declare project=$2
	else
		declare project=""
	fi

	activate_venv pyesdoc
	python $DIR_JOBS/archive/run_populate.py --throttle=$throttle --project=$project

	log "populated archive ..."
}
