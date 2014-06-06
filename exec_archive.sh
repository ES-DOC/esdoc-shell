# ###############################################################
# SECTION: ARCHIVE FUNCTIONS
# ###############################################################

# Resets archival directories.
_reset_archive_directories()
{
	for DIRECTORY in "${DIRECTORIES[@]}"
	do
		for SUB_DIRECTORY in $(find $DIR_ARCHIVE -type d -name $DIRECTORY)
		do
			rm $SUB_DIRECTORY/*.* 2> /dev/null
		done
	done
}

# Seeds the archive for the first time.
run_archive_seed()
{
	log "seeding archive ..."

    declare -a DIRECTORIES=(raw_error)
    _reset_archive_directories $DIRECTORIES

	activate_venv api
	python ./exec.py "archive-seed" $1

	log "seeded archive"
}

# Organizes the archive for the first time.
run_archive_organize()
{
    log "organizing archive ..."

    declare -a DIRECTORIES=(parsed_error)
    _reset_archive_directories $DIRECTORIES

	activate_venv api
	python ./exec.py "archive-organize" $1

    log "archive organized"
}

# Reorganizes the archive.
run_archive_reorganize()
{
    log "reorganizing archive ..."

    declare -a DIRECTORIES=(organized parsed parsed_error)
    _reset_archive_directories $DIRECTORIES

 	activate_venv api
	python ./exec.py "archive-organize" $1

    log "archive reorganized"
}

# Reseed the archive.
run_archive_reseed()
{
    log "reseeding archive ..."

    declare -a DIRECTORIES=(raw raw_error organized parsed parsed_error)
    _reset_archive_directories $DIRECTORIES

 	activate_venv api
	python ./exec.py "archive-seed" $1

    log "archive reseeding"
}
