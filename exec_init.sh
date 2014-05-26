#!/bin/bash

# ###############################################################
# SECTION: INIT
# ###############################################################

# Set path: db.
DIR_DB=$DIR/db

# Set path: repos.
DIR_REPOS=$DIR/repos

# Set path: templates.
DIR_TEMPLATES=$DIR/templates

# Set path: tmp.
DIR_TMP=$DIR/tmp

# Set path: venv.
DIR_VENV=$DIR/venv

# Set path: python.
DIR_PYTHON=$DIR_VENV/python

# Set path: source code: api
DIR_SRC_API=$DIR_REPOS/esdoc-api/src

# Set path: source code: meta-programming
DIR_SRC_MP=$DIR_REPOS/esdoc-mp/src

# Set path: source code: pyesdoc
DIR_SRC_PYESDOC=$DIR_REPOS/esdoc-py-client/src

# Set path: source code: questionnaire
DIR_SRC_QTN=$DIR_REPOS/esdoc-questionnaire/src

# Set path: source code: api
DIR_API=$DIR_SRC_API/esdoc_api

# Set path: tests: api
DIR_TESTS_API=$DIR_REPOS/esdoc-api/tests

# Set path: tests: meta-programming
DIR_TESTS_MP=$DIR_REPOS/esdoc-mp/tests

# Set path: tests: pyesdoc
DIR_TESTS_PYESDOC=$DIR_REPOS/esdoc-py-client/tests
DIR_TESTS_PYESDOC1=$DIR_REPOS/esdoc-py-client

# Set path: pyesdoc miscellaneous
DIR_MISC_PYESDOC=$DIR_REPOS/esdoc-py-client/misc

# Set action.
ACTION=`echo $1 | tr '[:upper:]' '[:lower:]' | tr '-' '_'`
if [[ $ACTION != run-* ]]; then
	ACTION="run_"$ACTION
fi

# Set action arguments.
ACTION_ARG1=$2
ACTION_ARG2=$3
ACTION_ARG3=$4

# List of git repos.
REPOS=(
	'esdoc-api'
	'esdoc-cv'
	'esdoc-docs'
	'esdoc-js-client'
	'esdoc-mp'
	'esdoc-py-client'
	'esdoc-questionnaire'
	'esdoc-splash'
	'esdoc-static'
	'esdoc-viewer'
)

# List of virtual environments.
VENVS=(
	'api'
	'mp'
	'questionnaire'
	'pyesdoc'
)

# ###############################################################
# SECTION: HELPER FUNCTIONS
# ###############################################################

# Wraps standard echo by adding ES-DOC prefix.
log()
{
	tabs=''
	if [ "$1" ]; then
		if [ "$2" ]; then
			for ((i=0; i<$2; i++))
			do
				tabs+='\t'
			done
	    	echo -e 'ES-DOC :: '$tabs$1
	    else
	    	echo -e "ES-DOC :: "$1
	    fi
	else
	    echo -e "ES-DOC ::"
	fi
}

log_banner()
{
	echo "---------------------------------------------"
}

# Outputs header information.
log_script_header()
{
	log "EXEC PATH: $DIR/exec.sh"
	log "EXEC COMMAND: ${1}"
	if [ "$2" ]; then
		log "EXEC COMMAND OPTION: ${2}"
	fi
}

# Assigns the current working directory.
set_working_dir()
{
	if [ "$1" ]; then
		cd $1
	else
		cd $DIR
	fi
}

# Resets temporary folder.
reset_tmp()
{
	rm -rf $DIR_TMP/*
	mkdir -p $DIR_TMP
}

# Activates a virtual environment.
activate_venv()
{
	log "Activating $1 virtual environment"

	if [ $1 = "api" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_SRC_API

	elif [ $1 = "qtn" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_SRC_QTN

	elif [ $1 = "mp" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_SRC_MP
		export PYTHONPATH=$PYTHONPATH:$DIR_TESTS_MP

	elif [ $1 = "pyesdoc" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_SRC_PYESDOC
		export PYTHONPATH=$PYTHONPATH:$DIR_TESTS_PYESDOC1
		export PYTHONPATH=$PYTHONPATH:$DIR_TESTS_PYESDOC
	fi

	source $DIR_VENV/$1/bin/activate
}

# ###############################################################
# SECTION: MAIN
# ###############################################################

# Initialise working directory.
set_working_dir

# Initialise temporary folder.
reset_tmp

# Load config.
if [ -a $DIR/exec.config ]; then
	source $DIR/exec.config

	# ... set default db host name.
	if [ ! $DB_HOSTNAME ]; then
		DB_HOSTNAME="localhost"
	fi;

	# ... set default db user name.
	if [ ! $DB_USERNAME ]; then
		DB_USERNAME="postgres"
	fi;
fi
