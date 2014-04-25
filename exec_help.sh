# ###############################################################
# SECTION: HELP
# ###############################################################

# Displays help information to user.
help()
{
	log "General commands :"
	log "boostrap" 1
	log "prepares system for install " 2
	log "install" 1
	log "installs esdoc shell, git repos & virtual environments" 2
	log "update" 1
	log "updates esdoc shell, git repos & virtual environments" 2
	log "uninstall" 1
	log "uninstalls esdoc shell, git repos & virtual environments" 2

	log ""
	log "API commands :"
	log "run-api" 1
	log "launches api web application" 2
	log "run-api-tests" 1
	log "executes api automated tests" 2
	log "run-api-comparator-setup" 1
	log "executes comparator setup" 2
	log "run-api-visualizer-setup" 1
	log "executes visualizer setup" 2
	log "run-api-stats" 1
	log "writes api statistics to file system" 2

	log ""
	log "Database commands :"
	log "run-db-setup" 1
	log "sets up database" 2
	log "run-db-ingest" 1
	log "ingests externally published documents" 2
	log "run-db-restore" 1
	log "restores database restore from deployment backup" 2

	log ""
	log "MP commands :"
	log "run-mp" 1
	log "builds pyesdoc from meta-programming framework" 2
	log "run-mp-tests" 1
	log "executes mp automated tests" 2
	log "run-mp-custom-schema" 1
	log "runs mp against a custom schema as proof of concept" 2

	log ""
	log "PYESDOC commands :"
	log "run-pyesdoc-tests" 1
	log "exec pyesdoc automated tests" 2
	log "run-pyesdoc-scenario" 1
	log "illustrates pyesdoc scenarios" 2

	log ""
	log "help" 1
	log "displays help text" 2
}
