#!/bin/bash

# ###############################################################
# SECTION: HELP
# ###############################################################

# Displays help text to user.
run_help()
{
	helpers=(
		run_help_stack
		run_help_api
		run_help_api_db
		run_help_archive
		run_help_js_plugin
		run_help_mp
	)

	log "------------------------------------------------------------------"
	for helper in "${helpers[@]}"
	do
		$helper
		log "------------------------------------------------------------------"
	done
}



run_help_api()
{
	log "API commands :"
	log "api" 1
	log "launches api web application" 2
	log "api-tests" 1
	log "executes api automated tests" 2
	log "api-write-comparator-setup-data" 1
	log "writes comparator setup data to file system" 2
	log "api-write-stats" 1
	log "writes api statistics to file system" 2
}

run_help_api_db()
{
	log "API DB commands :"
	log "api-db-ingest [THROTTLE] [TYPE]" 1
	log "ingests documents from pyesdoc archive" 2
	log "THROTTLE = limit on number of documents to ingest (0=all)" 2
	log "TYPE = type of document to ingest" 2
	log "api-db-index" 1
	log "builds document facet indexes" 2
	log "api-db-index-reset" 1
	log "deletes document facet indexes & then rebuilds" 2
	log "api-db-install" 1
	log "installs database" 2
	log "api-db-reset" 1
	log "uninstalls & installs database" 2
	log "api-db-uninstall" 1
	log "uninstalls database" 2

}

run_help_archive()
{
	log "Archive commands :"
	log "archive-seed" 1
	log "seeds archive with documents pulled from remote sources" 2
	log "archive-reset" 1
	log "deletes all document from archive" 2
	log "archive-organize" 1
	log "writes parsed documents to file system in a directory structure organized by document type" 2
	log "archive-organize-reset" 1
	log "deletes & then rebuilds organized document archive" 2
}

run_help_js_plugin()
{
	log "Javascript plugin commands :"
	log "js-plugin-compile" 1
	log "compiles es-doc javascript plugin" 2
}

run_help_mp()
{
	log "MP commands :"
	log "mp" 1
	log "builds pyesdoc from meta-programming framework" 2
	log "mp-tests" 1
	log "executes meta-programming utility automated tests" 2
	log "mp-custom-schema" 1
	log "runs meta-programming utility against a custom schema as proof of concept" 2
}

run_help_pyesdoc()
{
	log "PYESDOC commands :"
	log "pyesdoc-scenario" 1
	log "illustrates pyesdoc scenarios" 2
	log "pyesdoc-tests" 1
	log "exec pyesdoc automated tests" 2
	log "pyesdoc-write-test-files" 1
	log "writes test files used for pyesdoc unit tests" 2
	log "pyesdoc-write-demo-files" 1
	log "writes test files used for viewer demonstration" 2
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
