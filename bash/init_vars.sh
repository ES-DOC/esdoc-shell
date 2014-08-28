#!/bin/bash

# ###############################################################
# SECTION: INITIALIZE VARS
# ###############################################################

# List of git repos.
declare -a REPOS=(
	'esdoc-api'
	'esdoc-cv'
	'esdoc-cim'
	'esdoc-cim-cv'
	'esdoc-comparator'
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

# Load vars from config.
if [ -a $DIR/exec.sh.config ]; then
	source $DIR/exec.sh.config

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

	# ... set default document archive location.
	if [ ! $DIR_ARCHIVE ]; then
		declare DIR_ARCHIVE=$DIR_PYESDOC_SRC/pyesdoc/archive/documents
	fi;
fi
