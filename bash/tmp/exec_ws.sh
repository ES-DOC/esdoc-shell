# ###############################################################
# SECTION: API FUNCTIONS
# ###############################################################

# Launches web-service.
run_ws()
{
    log "WS : running ..."

	activate_venv ws
	python ./exec.py "ws-run"
}

# Executes api tests.
run_ws_tests()
{
    log "WS : running tests ..."

	activate_venv ws

	if [ ! "$1" ]; then
	    log "WS :: Executing tests"
	    nosetests -v -s $DIR_TESTS_WS
	fi
}

_ws_help()
{
	log ""
	log "Web service commands :"
	log "ws" 1
	log "launches web service application" 2
}