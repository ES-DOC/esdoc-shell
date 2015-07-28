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

    supervisorctl -c $DIR_CONFIG/web/api-supervisord.conf start all
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
