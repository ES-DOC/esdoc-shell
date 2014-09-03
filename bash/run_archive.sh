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
			log "deleting contents of "$SUB_DIRECTORY
			rm -rf $SUB_DIRECTORY 2> /dev/null
		done
	done
}

# Reset the archive.
run_archive_reset()
{
    log "resetting archive ..."
	_log_archive_location

    declare -a DIRECTORIES=(raw raw_error organized parsed parsed_error)
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
	python $DIR_JOBS/archive/populate.py $1

	log "populated archive ..."
}

# Parses downloaded documents.
run_archive_parse()
{
	log "parsing archive ..."
	_log_archive_location

    declare -a DIRECTORIES=(parsed_error)
    reset_archive_directories $DIRECTORIES

	activate_venv pyesdoc
	python $DIR_JOBS/archive/parse.py $1

	log "parsed archive"
}

# Organizes the archive for the first time.
run_archive_organize()
{
    log "organizing archive ..."
	_log_archive_location

    declare -a DIRECTORIES=(parsed_error)
    reset_archive_directories $DIRECTORIES

	activate_venv pyesdoc
	python $DIR_JOBS/archive/organize.py $1

    log "archive organized"
}

# Reorganizes the archive.
run_archive_organize_reset()
{
    log "resetting & reorganizing archive ..."
	_log_archive_location

    declare -a DIRECTORIES=(organized parsed parsed_error)
    reset_archive_directories $DIRECTORIES

	activate_venv pyesdoc
	python $DIR_JOBS/archive/organize.py $1

    log "archive reorganized"
}
