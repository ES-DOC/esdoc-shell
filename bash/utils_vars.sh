#!/bin/bash

# ###############################################################
# SECTION: PATHS
# ###############################################################

# Define core directories.
declare ESDOC_DIR_BASH=$ESDOC_HOME/bash
declare ESDOC_DIR_REPOS=$ESDOC_HOME/repos
declare ESDOC_DIR_REPOS_CORE=$ESDOC_DIR_REPOS/core
declare ESDOC_DIR_REPOS_EXT=$ESDOC_DIR_REPOS/ext

# Define repo directories.
declare ESDOC_DIR_CIM=$ESDOC_DIR_REPOS_CORE/esdoc-cim
declare ESDOC_DIR_PYESDOC=$ESDOC_DIR_REPOS_CORE/esdoc-py-client

# ###############################################################
# SECTION: VARS
# ###############################################################

# Set of core git repos.
declare -a ESDOC_REPOS_CORE=(
	'https://github.com/ES-DOC/esdoc-api.git'
	'https://github.com/ES-DOC/esdoc-archive.git'
	'https://github.com/ES-DOC/esdoc-cdf2cim.git'
	'https://github.com/ES-DOC/esdoc-cdf2cim-archive.git'
	'https://github.com/ES-DOC/esdoc-cdf2cim-indexer.git'
	'https://github.com/ES-DOC/esdoc-cdf2cim-ws.git'
	'https://github.com/ES-DOC/esdoc-cim.git'
	'https://github.com/ES-DOC/esdoc-cim-v1-schema.git'
	'https://github.com/ES-DOC/esdoc-cim-v2-schema.git'
	'https://github.com/ES-DOC/esdoc-docs.git'
	'https://github.com/ES-DOC/esdoc-errata-client.git'
	'https://github.com/ES-DOC/esdoc-errata-fe.git'
	'https://github.com/ES-DOC/esdoc-errata-ws.git'
	'https://github.com/ES-DOC/esdoc-py-client.git'
	'https://github.com/ES-DOC/esdoc-web-compare.git'
	'https://github.com/ES-DOC/esdoc-web-explorer.git'
	'https://github.com/ES-DOC/esdoc-web-search.git'
	'https://github.com/ES-DOC/esdoc-web-view.git'
	'https://github.com/ES-DOC/esdoc-web-view-specialization.git'
	'https://github.com/ES-DOC/esdoc-ws-url-rewriter.git'
	'https://github.com/ES-DOC/pyessv.git'
	'https://github.com/ES-DOC/pyessv-archive.git'
	'https://github.com/ES-DOC/pyessv-js.git'
	'https://github.com/ES-DOC/pyessv-writers.git'
	'https://github.com/ES-DOC/pyessv-ws.git'
)

# Set of external git repos.
declare -a ESDOC_REPOS_EXT=(
	'https://github.com/ESGF/esgf-config.git'
	'https://github.com/ESGF/esgf-prepare.git'
	'https://github.com/WCRP-CMIP/CMIP6_CVs.git'
)
