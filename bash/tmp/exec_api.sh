# ###############################################################
# SECTION: API FUNCTIONS
# ###############################################################

# Launches api web-service.
run_api()
{
    log "API : running ..."

	activate_venv api
	paster serve --reload $DIR_API_SRC/esdoc_api/config/ini_files/config.ini
}

# Executes api tests.
run_api_tests()
{
    log "API : running tests ..."

	activate_venv api

	if [ ! "$1" ]; then
	    log "API :: Executing api tests"
	    nosetests -v -s $DIR_API_TESTS/esdoc_api_test
	fi
}

# Executes api comparator setup.
run_api_comparator_setup()
{
    log "API : setting up comparator ..."

    # Generate data.
	activate_venv api
	python ./exec.py "api-setup-comparator"

	# Copy to static files.
	cp $DIR_REPOS/esdoc-api/src/esdoc_api/static/json/compare.setup*.* $DIR_REPOS/esdoc-static/data

	# Copy to js demo.
	cp $DIR_REPOS/esdoc-api/src/esdoc_api/static/json/compare.setup*.* $DIR_REPOS/esdoc-js-client/demo
}

# Executes api stats.
run_api_stats()
{
    log "API : writing stats ..."

    # Generate data.
	activate_venv api
	python ./exec.py "api-stats"

	# Copy to static files.
	cp $DIR_REPOS/esdoc-api/src/esdoc_api/static/csv/doc_stats.* $DIR_REPOS/esdoc-static/data
	cp $DIR_REPOS/esdoc-api/src/esdoc_api/static/json/doc_stats.* $DIR_REPOS/esdoc-static/data
}

# Executes api visualizer setup.
run_api_visualizer_setup()
{
    log "API : setting up visualizer ..."

    # Generate data.
	activate_venv api
	python ./exec.py "api-setup-visualizer"

	# Copy to static files.
	cp $DIR_REPOS/esdoc-api/src/esdoc_api/static/json/visualize.setup*.* $DIR_REPOS/esdoc-static/data
}

_api_help()
{
	log ""
	log "API commands :"
	log "api" 1
	log "launches api web application" 2
	log "api-tests" 1
	log "executes api automated tests" 2
	log "api-comparator-setup" 1
	log "writes comparator setup data to file system" 2
	log "api-visualizer-setup" 1
	log "writes visualizer setup data to file system" 2
	log "api-stats" 1
	log "writes api statistics to file system" 2
}