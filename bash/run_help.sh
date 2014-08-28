#!/bin/bash

# ###############################################################
# SECTION: HELP
# ###############################################################

# Displays help text to user.
run_help()
{
	helpers=(
		run_help_stack
		run_help_db
		run_help_api
	)

	log "------------------------------------------------------------------"
	for helper in "${helpers[@]}"
	do
		$helper
		log "------------------------------------------------------------------"
	done
}

run_help_db()
{
	log "DB commands :"
	log "db-backup" 1
	log "performs a backup of database" 2
	log "db-install" 1
	log "initializes database" 2
	log "db-reset" 1
	log "uninstalls & installs database" 2
	log "db-restore" 1
	log "restores database from backup" 2
	log "db-uninstall" 1
	log "drops database" 2
}

run_help_api()
{
	log "API commands :"
	log "api" 1
	log "launches api web application" 2
	log "api-comparator-setup" 1
	log "writes comparator setup data to file system" 2
	log "api-tests" 1
	log "executes api automated tests" 2
	log "api-stats" 1
	log "writes api statistics to file system" 2
}


run_help_stack()
{
	log "Stack commands :"
	log "stack-bootstrap" 1
	log "prepares system for install " 2
	log "stack-install" 1
	log "installs stack & virtual environments" 2
	log "stack-update" 1
	log "updates full stack (i.e. repos, config and virtual environments)" 2
	log "stack-update-shell" 1
	log "updates shell" 2
	log "stack-update-repos" 1
	log "updates git repos" 2
	log "stack-update-venvs" 1
	log "updates virtual environments" 2
	log "stack-uninstall" 1
	log "uninstalls stack & virtual environments" 2
}
