#!/bin/bash

# ###############################################################
# SECTION: INITIALIZE ACTION
# ###############################################################

# Set action.
declare ACTION=`echo $1 | tr '[:upper:]' '[:lower:]' | tr '-' '_'`
if [[ $ACTION != run_* ]]; then
	declare ACTION="run_"$ACTION
fi

# Set action arguments.
declare ACTION_ARG1=$2
declare ACTION_ARG2=$3
declare ACTION_ARG3=$4
declare ACTION_ARG4=$5

# ###############################################################
# SECTION: HELPER FUNCTIONS
# ###############################################################

# Activates a virtual environment.
activate_venv()
{
	if [ $1 = "api" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_PYESDOC
		export PYTHONPATH=$PYTHONPATH:$DIR_API
		export PYTHONPATH=$PYTHONPATH:$DIR_API_TESTS

	elif [ $1 = "qtn" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_QTN_SRC

	elif [ $1 = "mp" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_MP
		export PYTHONPATH=$PYTHONPATH:$DIR_MP_TESTS

	elif [ $1 = "pyesdoc" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_PYESDOC
		export PYTHONPATH=$PYTHONPATH:$DIR_PYESDOC_TESTS
	fi

	source $DIR_VENV/$1/bin/activate
}

# Wraps standard echo by adding PRODIGUER prefix.
log()
{
	declare tabs=''
	if [ "$1" ]; then
		if [ "$2" ]; then
			for ((i=0; i<$2; i++))
			do
				declare tabs+='\t'
			done
	    	echo -e 'ES-DOC INFO SH > '$tabs$1
	    else
	    	echo -e "ES-DOC INFO SH > "$1
	    fi
	else
	    echo -e ""
	fi
}

# Outputs a line to split up logging.
log_banner()
{
	echo "-------------------------------------------------------------------------------"
}

# Resets temporary folder.
reset_tmp()
{
	rm -rf $DIR_TMP/*
	mkdir -p $DIR_TMP
}

# Assigns the current working directory.
set_working_dir()
{
	if [ "$1" ]; then
		cd $1
	else
		cd $ESDOC_HOME
	fi
}

# Removes all files of passed type in current working directory.
remove_files()
{
	find . -name $1 -exec rm -rf {} \;
}

# ###############################################################
# SECTION: INITIALIZE PATHS
# ###############################################################

declare DIR_DEFAULT_ARCHIVE=$ESDOC_HOME/archive
declare DIR_BACKUPS=$ESDOC_HOME/ops/backups
declare DIR_BASH=$ESDOC_HOME/bash
declare DIR_CONFIG=$ESDOC_HOME/ops/config
declare DIR_DAEMONS=$ESDOC_HOME/ops/daemons
declare DIR_LOGS=$ESDOC_HOME/ops/logs
declare DIR_PYTHON=$ESDOC_HOME/ops/venv/python
declare DIR_REPOS=$ESDOC_HOME/repos
declare DIR_RESOURCES=$ESDOC_HOME/resources
declare DIR_TMP=$ESDOC_HOME/ops/tmp
declare DIR_VENV=$ESDOC_HOME/ops/venv

declare DIR_API=$DIR_REPOS/esdoc-api
declare DIR_API_TESTS=$DIR_REPOS/esdoc-api/tests

declare DIR_MP=$DIR_REPOS/esdoc-mp
declare DIR_MP_TESTS=$DIR_REPOS/esdoc-mp/tests

declare DIR_PYESDOC=$DIR_REPOS/esdoc-py-client
declare DIR_PYESDOC_TESTS=$DIR_REPOS/esdoc-py-client/tests

declare DIR_QTN_SRC=$DIR_REPOS/esdoc-questionnaire/src

declare DIR_WEB_COMPARATOR=$DIR_REPOS/esdoc-comparator
declare DIR_WEB_PLUGIN=$DIR_REPOS/esdoc-js-client
declare DIR_WEB_STATIC=$DIR_REPOS/esdoc-static
declare DIR_WEB_VIEWER=$DIR_REPOS/esdoc-viewer


# Define core directories.
declare ESDOC_DIR_BASH=$ESDOC_HOME/bash
declare ESDOC_DIR_REPOS=$ESDOC_HOME/repos
declare ESDOC_DIR_DAEMONS=$ESDOC_HOME/ops/daemons
declare ESDOC_DIR_RESOURCES=$ESDOC_HOME/resources
declare ESDOC_DIR_TMP=$ESDOC_HOME/ops/tmp

# Define derived directories.
declare ESDOC_DIR_API=$ESDOC_DIR_REPOS/esdoc-api
declare ESDOC_DIR_API_TESTS=$ESDOC_DIR_REPOS/esdoc-api/tests
declare ESDOC_DIR_MP=$ESDOC_DIR_REPOS/esdoc-mp
declare ESDOC_DIR_MP_TESTS=$ESDOC_DIR_REPOS/esdoc-mp/tests
declare ESDOC_DIR_PYESDOC=$DIR_REPOS/esdoc-py-client
declare ESDOC_DIR_PYESDOC_TESTS=$DIR_REPOS/esdoc-py-client/tests
declare ESDOC_DIR_WEB_COMPARATOR=$ESDOC_DIR_REPOS/esdoc-comparator
declare ESDOC_DIR_WEB_PLUGIN=$ESDOC_DIR_REPOS/esdoc-js-client
declare ESDOC_DIR_WEB_STATIC=$ESDOC_DIR_REPOS/esdoc-static
declare ESDOC_DIR_WEB_VIEWER=$DIR_REPOS/esdoc-viewer

# Ensure ops paths exist.
mkdir -p $ESDOC_DIR_DAEMONS
mkdir -p $ESDOC_DIR_DAEMONS/api
mkdir -p $ESDOC_DIR_TMP

# Clear temp files.
reset_tmp

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

source $ESDOC_HOME/bash/run_stack.sh
