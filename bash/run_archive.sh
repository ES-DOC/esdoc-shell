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

# Organizes the archive for the first time.
run_archive_organize()
{
    log "organizing archive ..."

	activate_venv pyesdoc

	if [ "$1" ]; then
		python $DIR_JOBS/archive/run_organize.py --organize_limit=$1
	else
		python $DIR_JOBS/archive/run_organize.py --organize_limit=0
	fi

    log "archive organized"
}

# Pulls documents from remote sources into the archive.
run_archive_populate()
{
	log "populating archive ..."

	activate_venv pyesdoc

	if [ "$1" ]; then
		python $DIR_JOBS/archive/run_populate.py --populate_limit=$1
	else
		python $DIR_JOBS/archive/run_populate.py --populate_limit=0
	fi

	log "populated archive ..."
}
