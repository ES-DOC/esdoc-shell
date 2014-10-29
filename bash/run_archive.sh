#!/bin/bash

# ###############################################################
# SECTION: ARCHIVE FUNCTIONS
# ###############################################################

# Logs location of archive.
_log_archive_location()
{
	log "archive location = "$DIR_ARCHIVE
}

# Resets archival directories.
reset_archive_directories()
{
	for DIRECTORY in "${DIRECTORIES[@]}"
	do
		for SUB_DIRECTORY in $(find $DIR_ARCHIVE -type d -name $DIRECTORY)
		do
			# log "deleting contents of "$SUB_DIRECTORY
			rm -rf $SUB_DIRECTORY 2> /dev/null
		done
	done
}

# Reset the archive.
run_archive_reset()
{
    log "resetting archive ..."
	_log_archive_location

    declare -a DIRECTORIES=(ingested ingested_error organized organized_error parsed parsed_error raw raw_error)
    reset_archive_directories $DIRECTORIES

    log "archive reset"
}

# Pulls documents from remote sources into the archive.
run_archive_populate()
{
	log "populating archive ..."
	_log_archive_location

    declare -a DIRECTORIES=(raw_error)
    reset_archive_directories $DIRECTORIES

	activate_venv pyesdoc

	if [ "$1" ]; then
		python $DIR_JOBS/archive/run_populate.py --populate_limit=$1
	else
		python $DIR_JOBS/archive/run_populate.py --populate_limit=0
	fi

	log "populated archive ..."
}

# Organizes the archive for the first time.
run_archive_organize()
{
    log "organizing archive ..."
	_log_archive_location

    declare -a DIRECTORIES=(parsed_error organized_error)
    reset_archive_directories $DIRECTORIES

	activate_venv pyesdoc

	if [ "$1" ]; then
		python $DIR_JOBS/archive/run_organize.py --organize_limit=$1
	else
		python $DIR_JOBS/archive/run_organize.py --organize_limit=0
	fi

    log "archive organized"
}

# Reorganizes the archive.
run_archive_organize_reset()
{
    log "resetting & reorganizing archive ..."
	_log_archive_location

    declare -a DIRECTORIES=(organized organized_error parsed parsed_error)
    reset_archive_directories $DIRECTORIES

	activate_venv pyesdoc

	if [ "$1" ]; then
		python $DIR_JOBS/archive/run_organize.py --organize_limit=$1
	else
		python $DIR_JOBS/archive/run_organize.py --organize_limit=0
	fi

    log "archive reorganized"
}

# Echos contents of an archived file.
run_archive_echo()
{
	activate_venv pyesdoc
	python $DIR_JOBS/archive/run_echo.py --uid=$1 --version=$2
}
