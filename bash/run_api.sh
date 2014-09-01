#!/bin/bash

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

# Writes api stats to file system.
run_api_write_stats()
{
    log "API : writing stats ..."

	activate_venv api

	python $DIR_JOBS/api/run_write_stats.py $DIR_WEB_STATIC/data

    log "API : stats written ---> esdoc/repos/esdoc-static/data "
}

# Executes api comparator setup.
run_api_write_comparator_setup_data()
{
    log "API : setting up comparator setup data ..."

	activate_venv api

	python $DIR_JOBS/api/run_write_comparator_setup.py $DIR_WEB_STATIC/data

	cp $DIR_WEB_STATIC/data/compare.setup*.* $DIR_REPOS/esdoc-js-client/demo

    log "API : comparator setup data written ---> esdoc/repos/esdoc-static/data"
    log "API : comparator setup data written ---> esdoc/repos/esdoc-js-client/demo"
}
