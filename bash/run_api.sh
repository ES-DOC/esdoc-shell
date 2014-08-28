# ###############################################################
# SECTION: API FUNCTIONS
# ###############################################################

# Launches api web-service.
run_api()
{
    log "API : running ..."

	activate_venv api

	python $DIR_SCRIPTS/jobs/api/run_api.py
}

# Executes api tests.
run_api_tests()
{
    log "API : running tests ..."

	activate_venv api

	if [ ! "$1" ]; then
	    log "API :: Executing tests"
	    nosetests -v -s $DIR_API_TESTS
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

