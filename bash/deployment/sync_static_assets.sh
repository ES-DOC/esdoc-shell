#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
	log "PYESDOC : syncing static assets ..."

	cp -r $ESDOC_DIR_REPOS_CORE/esdoc-web-plugin/bin/latest/* $ESDOC_DIR_REPOS_CORE/esdoc-web-static
	cp -r $ESDOC_DIR_REPOS_CORE/esdoc-web-plugin/bin/latest/images $ESDOC_DIR_REPOS_CORE/esdoc-web-static

	mkdir -p $ESDOC_DIR_REPOS_CORE/esdoc-web-static/ontologies/cim/1
	cp -r $ESDOC_DIR_REPOS_CORE/esdoc-cim/v1/xsd/*.xsd $ESDOC_DIR_REPOS_CORE/esdoc-web-static/ontologies/cim/1

	mkdir -p $ESDOC_DIR_REPOS_CORE/esdoc-web-static/cmip6
	cp -r $ESDOC_DIR_REPOS_CORE/esdoc-docs/cmip6/experiments/spreadsheet/experiments.xlsx $ESDOC_DIR_REPOS_CORE/esdoc-web-static/cmip6

	log "PYESDOC : static assets synced ..."
}

# Invoke entry point.
main
