# ###############################################################
# SECTION: ARCHIVE FUNCTIONS
# ###############################################################

# Executes archive build process.
run_archive_build()
{
	log "ARCHIVE : building ..."

	activate_venv api
	python ./exec.py "archive-build" $1

	log "ARCHIVE : built"
}
