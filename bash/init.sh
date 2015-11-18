#!/bin/bash

# ###############################################################
# SECTION: HELPER FUNCTIONS
# ###############################################################

# Activates a virtual environment.
activate_venv()
{
	if [ $1 = "api" ]; then
		export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_PYESDOC
		export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_API
		export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_API_TESTS

	elif [ $1 = "qtn" ]; then
		export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_QTN/src

	elif [ $1 = "mp" ]; then
		export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_MP
		export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_MP_TESTS

	elif [ $1 = "pyesdoc" ]; then
		export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_PYESDOC
		export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_PYESDOC_TESTS
	fi

	source $ESDOC_DIR_VENV/$1/bin/activate
}

# Wraps standard echo by adding ESDOC prefix.
log()
{
	declare now=`date +%Y-%m-%dT%H:%M:%S`
	declare tabs=''
	if [ "$1" ]; then
		if [ "$2" ]; then
			for ((i=0; i<$2; i++))
			do
				declare tabs+='\t'
			done
	    	echo -e $now" [INFO] :: ES-DOC SH > "$tabs$1
	    else
	    	echo -e $now" [INFO] :: ES-DOC SH > "$1
	    fi
	else
	    echo -e $now" [INFO] :: ES-DOC SH > "
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
	rm -rf $ESDOC_DIR_TMP/*
	mkdir -p $ESDOC_DIR_TMP
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

# Define core directories.
declare ESDOC_DIR_ARCHIVE=$ESDOC_HOME/archive
declare ESDOC_DIR_BASH=$ESDOC_HOME/bash
declare ESDOC_DIR_DOCS=$ESDOC_HOME/docs
declare ESDOC_DIR_OPS=$ESDOC_HOME/ops
declare ESDOC_DIR_REPOS=$ESDOC_HOME/repos
declare ESDOC_DIR_RESOURCES=$ESDOC_HOME/resources

# Define ops sub-directories.
declare ESDOC_DIR_BACKUPS=$ESDOC_DIR_OPS/backups
declare ESDOC_DIR_CONFIG=$ESDOC_DIR_OPS/config
declare ESDOC_DIR_DAEMONS=$ESDOC_DIR_OPS/daemons
declare ESDOC_DIR_LOGS=$ESDOC_DIR_OPS/logs
declare ESDOC_DIR_PYTHON=$ESDOC_DIR_OPS/venv/python
declare ESDOC_DIR_TMP=$ESDOC_DIR_OPS/tmp
declare ESDOC_DIR_VENV=$ESDOC_DIR_OPS/venv

# Define repo directories.
declare ESDOC_DIR_API=$ESDOC_DIR_REPOS/esdoc-api
declare ESDOC_DIR_API_TESTS=$ESDOC_DIR_REPOS/esdoc-api/tests
declare ESDOC_DIR_MP=$ESDOC_DIR_REPOS/esdoc-mp
declare ESDOC_DIR_MP_TESTS=$ESDOC_DIR_REPOS/esdoc-mp/tests
declare ESDOC_DIR_PYESDOC=$ESDOC_DIR_REPOS/esdoc-py-client
declare ESDOC_DIR_PYESDOC_TESTS=$ESDOC_DIR_REPOS/esdoc-py-client/tests
declare ESDOC_DIR_QTN=$ESDOC_DIR_REPOS/esdoc-questionnaire
declare ESDOC_DIR_WEB_COMPARATOR=$ESDOC_DIR_REPOS/esdoc-comparator
declare ESDOC_DIR_WEB_PLUGIN=$ESDOC_DIR_REPOS/esdoc-js-client
declare ESDOC_DIR_WEB_STATIC=$ESDOC_DIR_REPOS/esdoc-static
declare ESDOC_DIR_WEB_VIEWER=$ESDOC_DIR_REPOS/esdoc-viewer

# Set of ops sub-directories.
declare -a ESDOC_OPS_DIRS=(
	$ESDOC_DIR_OPS
	$ESDOC_DIR_BACKUPS
	$ESDOC_DIR_CONFIG
	$ESDOC_DIR_DAEMONS
	$ESDOC_DIR_DAEMONS/api
	$ESDOC_DIR_LOGS
	$ESDOC_DIR_LOGS/api
	$ESDOC_DIR_TMP
	$ESDOC_DIR_VENV
	$ESDOC_DIR_PYTHON
)

# ###############################################################
# SECTION: INITIALIZE VARS
# ###############################################################

# Set of ops sub-directories.
declare -a ESDOC_OPS_DIRS=(
	$ESDOC_DIR_OPS
	$ESDOC_DIR_BACKUPS
	$ESDOC_DIR_CONFIG
	$ESDOC_DIR_DAEMONS
	$ESDOC_DIR_DAEMONS/api
	$ESDOC_DIR_LOGS
	$ESDOC_DIR_LOGS/api
	$ESDOC_DIR_TMP
	$ESDOC_DIR_VENV
	$ESDOC_DIR_PYTHON
)

# Set of git repos.
declare -a ESDOC_REPOS=(
	'esdoc-api'
	'esdoc-cim'
	'esdoc-cim-cv'
	'esdoc-comparator'
	'esdoc-contrib'
	'esdoc-cv'
	'esdoc-docs'
	'esdoc-docs-cmip6'
	'esdoc-js-client'
	'esdoc-mp'
	'esdoc-py-client'
	'esdoc-questionnaire'
	'esdoc-search'
	'esdoc-splash'
	'esdoc-static'
	'esdoc-viewer'
)

# Set of virtual environments.
declare -a ESDOC_VENVS=(
	'api'
	'mp'
	'questionnaire'
	'pyesdoc'
)

# ###############################################################
# SECTION: Initialise file system
# ###############################################################

# Ensure ops paths exist.
for ops_dir in "${ESDOC_OPS_DIRS[@]}"
do
	mkdir -p $ops_dir
done

# Clear temp files.
reset_tmp