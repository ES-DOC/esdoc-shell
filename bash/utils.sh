#!/bin/bash

# ###############################################################
# SECTION: HELPER FUNCTIONS
# ###############################################################

# Activates a virtual environment.
activate_venv()
{
	export PYTHONPATH=$PYTHONPATH:$PYESDOC_HOME
	source $PYESDOC_HOME/ops/venv/bin/activate
}

# Wraps standard echo by adding ESDOC prefix.
log()
{
	declare now=`date +%Y-%m-%dT%H:%M:%S:000000`
	declare tabs=''
	if [ "$1" ]; then
		if [ "$2" ]; then
			for ((i=0; i<$2; i++))
			do
				declare tabs+='\t'
			done
	    	echo -e $now" [INFO] :: ESDOC-SH :: "$tabs$1
	    else
	    	echo -e $now" [INFO] :: ESDOC-SH :: "$1
	    fi
	else
	    echo -e $now" [INFO] :: ESDOC-SH :: "
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

activate_sub_shells()
{
	source $ESDOC_HOME/repos/esdoc-api/sh/activate
	source $ESDOC_HOME/repos/esdoc-archive/sh/activate
	source $ESDOC_HOME/repos/esdoc-py-client/sh/activate
	source $ESDOC_HOME/repos/esdoc-cdf2cim/sh/activate
	source $ESDOC_HOME/repos/esdoc-cdf2cim-ws/sh/activate
	source $ESDOC_HOME/repos/esdoc-errata-ws/sh/activate
	source $ESDOC_HOME/repos/esdoc-web-plugin/sh/activate
}

# ###############################################################
# SECTION: INITIALIZE PATHS
# ###############################################################

# Define core directories.
declare ESDOC_DIR_BASH=$ESDOC_HOME/bash
declare ESDOC_DIR_DOCS=$ESDOC_HOME/docs
declare ESDOC_DIR_OPS=$ESDOC_HOME/ops
declare ESDOC_DIR_REPOS=$ESDOC_HOME/repos
declare ESDOC_DIR_REPOS_CORE=$ESDOC_DIR_REPOS/core
declare ESDOC_DIR_REPOS_CMIP6=$ESDOC_DIR_REPOS/cmip6
declare ESDOC_DIR_REPOS_INSTITUTIONAL=$ESDOC_DIR_REPOS/institutional
declare ESDOC_DIR_REPOS_MISC=$ESDOC_DIR_REPOS/misc
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
declare ESDOC_DIR_API=$ESDOC_DIR_REPOS_CORE/esdoc-api
declare ESDOC_DIR_API_TESTS=$ESDOC_DIR_REPOS_CORE/esdoc-api/tests
declare ESDOC_DIR_ARCHIVE=$ESDOC_DIR_REPOS_CORE/esdoc-archive
declare ESDOC_DIR_CIM=$ESDOC_DIR_REPOS_CORE/esdoc-cim
declare ESDOC_DIR_PYESDOC=$ESDOC_DIR_REPOS_CORE/esdoc-py-client
declare ESDOC_DIR_PYESDOC_TESTS=$ESDOC_DIR_REPOS_CORE/esdoc-py-client/tests
declare ESDOC_DIR_WEB_COMPARATOR=$ESDOC_DIR_REPOS_CORE/esdoc-web-compare
declare ESDOC_DIR_WEB_PLUGIN=$ESDOC_DIR_REPOS_CORE/esdoc-web-plugin

# Project specific.
declare ESDOC_DIR_CMIP6=$ESDOC_DIR_REPOS_CMIP6

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

# Set of core git repos.
declare -a ESDOC_REPOS_CORE=(
	'esdoc-api'
	'esdoc-cdf2cim'
	'esdoc-cdf2cim-archive'
	'esdoc-cdf2cim-ws'
	'esdoc-cim'
	'esdoc-cim-v1-schema'
	'esdoc-cim-v2-schema'
	'esdoc-docs'
	'esdoc-errata-client'
	'esdoc-errata-fe'
	'esdoc-errata-ws'
	'esdoc-py-client'
	'esdoc-web-compare'
	'esdoc-web-demo'
	'esdoc-web-plugin'
	'esdoc-web-search'
	'esdoc-web-static'
	'esdoc-web-view'
	'esdoc-web-view-furtherinfo'
	'esdoc-web-view-specialization'
	'esdoc-ws-url-rewriter'
	'pyessv'
	'pyessv-archive'
	'pyessv-js'
)

# Set of cmip6 git repos.
declare -a ESDOC_REPOS_CMIP6=(
	'cmip6-specializations-toplevel'
	'cmip6-specializations-seaice'
	'cmip6-specializations-ocnbgchem'
	'cmip6-specializations-ocean'
	'cmip6-specializations-landice'
	'cmip6-specializations-land'
	'cmip6-specializations-atmoschem'
	'cmip6-specializations-atmos'
	'cmip6-specializations-aerosol'
)

# Set of cmip6 git repos.
declare -a ESDOC_REPOS_MISC=(
	'https://github.com/ESGF/esgf-config.git'
	'https://github.com/ESGF/esgf-prepare.git'
)

# Set of virtual environments.
declare -a ESDOC_VENVS=(
	'api'
	'pyesdoc'
)

# Vocabs.
source $ESDOC_DIR_BASH/utils_vocabs.sh

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
