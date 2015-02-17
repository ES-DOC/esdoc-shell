#!/bin/bash

# ###############################################################
# SECTION: INITIALIZE VARS
# ###############################################################

# List of git repos.
declare -a REPOS=(
	'esdoc-api'
	'esdoc-cim'
	'esdoc-cim-cv'
	'esdoc-comparator'
	'esdoc-contrib'
	'esdoc-cv'
	'esdoc-docs'
	'esdoc-js-client'
	'esdoc-mp'
	'esdoc-py-client'
	'esdoc-questionnaire'
	'esdoc-search'
	'esdoc-splash'
	'esdoc-static'
	'esdoc-viewer'
)

# List of virtual environments.
declare -a VENVS=(
	'api'
	'mp'
	'questionnaire'
	'pyesdoc'
)

# Vars config.
if [ -a $DIR_CONFIG/esdoc.sh ]; then
	# ... load config.
	source $DIR_CONFIG/esdoc.sh
fi

# ... set default python version.
if [ ! $PYTHON_VERSION ]; then
	declare PYTHON_VERSION="2.7.8"
fi;

# ... set default db host name.
if [ ! $DB_HOSTNAME ]; then
	declare DB_HOSTNAME="localhost"
fi;

# ... set default db user name.
if [ ! $DB_USERNAME ]; then
	declare DB_USERNAME="postgres"
fi;
