#!/bin/bash

# ###############################################################
# SECTION: API FUNCTIONS
# ###############################################################

# Launches api web-service.
run_api()
{
    log "API : running ..."

	activate_venv api

	python $DIR_API/jobs/run_api.py
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

	python $DIR_API/jobs/run_write_stats.py --outdir=$DIR_API_STATIC/data

    log "API : stats written ---> esdoc/repos/esdoc-static/data "
}

# Executes api comparator setup.
run_api_write_comparator_setup_data()
{
    log "API : setting up comparator setup data ..."

	activate_venv api

	python $DIR_API/jobs/run_write_comparator_setup.py --outdir=$DIR_API_STATIC/data

	cp $DIR_API_STATIC/data/compare.setup*.* $DIR_API_COMPARATOR/src/data

    log "API : comparator setup data written ---> esdoc/repos/esdoc-static/data"
    log "API : comparator setup data written ---> esdoc/repos/esdoc-comparator/src/data"
}

# Initializes API daemon.
run_api_daemon_init()
{
    run_api_daemon_reset_logs

    activate_venv api

    supervisord -c $DIR_CONFIG/api-supervisord.conf
}

# Kills API daemon process.
run_api_daemon_kill()
{
    activate_venv api

 	 supervisorctl -c $DIR_CONFIG/api-supervisord.conf stop all
     supervisorctl -c $DIR_CONFIG/api-supervisord.conf shutdown
}

# Restarts API daemons.
run_api_daemon_refresh()
{
    activate_venv api

    supervisorctl -c $DIR_CONFIG/api-supervisord.conf stop all
    supervisorctl -c $DIR_CONFIG/api-supervisord.conf update all
    supervisorctl -c $DIR_CONFIG/api-supervisord.conf start all
}

# Resets API daemon logs.
run_api_daemon_reset_logs()
{
    rm $DIR_DAEMONS/*.log
}

# Restarts API daemons.
run_api_daemon_restart()
{
    activate_venv api

    supervisorctl -c $DIR_CONFIG/api-supervisord.conf stop all
    supervisorctl -c $DIR_CONFIG/api-supervisord.conf start all
}

# Launches API daemons.
run_api_daemon_start()
{
    activate_venv api

    supervisorctl -c $DIR_DAEMONS/web/api-supervisord.conf start all
}

# Launches API daemons.
run_api_daemon_status()
{
    activate_venv api

    supervisorctl -c $DIR_CONFIG/api-supervisord.conf status all
}

# Launches API daemons.
run_api_daemon_stop()
{
    activate_venv api

    supervisorctl -c $DIR_CONFIG/api-supervisord.conf stop all
}

# Updates the web supervisord config file.
run_api_daemon_update_config()
{
    cp $DIR_RESOURCES/deployment/template-api-supervisord.conf $DIR_CONFIG/api-supervisord.conf
}
