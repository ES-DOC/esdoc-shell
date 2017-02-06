#!/bin/bash

# ###############################################################
# SECTION: HELPER VARS
# ###############################################################

# Set git-hub protocol.
declare ESDOC_GIT_PROTOCOL=${ESDOC_GIT_PROTOCOL:='https'}

# ###############################################################
# SECTION: HELPER FUNCTIONS
# ###############################################################

# Activates a virtual environment.
activate_venv()
{
	if [ $1 = "pyesdoc" ]; then
		export PYTHONPATH=$PYTHONPATH:$PYESDOC_HOME
		export PYTHONPATH=$PYTHONPATH:$PYESDOC_HOME/tests
		source $PYESDOC_HOME/ops/venv/bin/activate
	fi
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
declare ESDOC_DIR_ARCHIVE=$ESDOC_DIR_REPOS/esdoc-archive
declare ESDOC_DIR_CIM=$ESDOC_DIR_REPOS/esdoc-cim
declare ESDOC_DIR_PYESDOC=$ESDOC_DIR_REPOS/esdoc-py-client
declare ESDOC_DIR_PYESDOC_TESTS=$ESDOC_DIR_REPOS/esdoc-py-client/tests

declare ESDOC_DIR_WEB_COMPARATOR=$ESDOC_DIR_REPOS/esdoc-web-compare
declare ESDOC_DIR_WEB_PLUGIN=$ESDOC_DIR_REPOS/esdoc-web-plugin

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
	'cmip6-specializations-aerosols'
	'cmip6-specializations-atmosphere'
	'cmip6-specializations-atmospheric-chemistry'
	'cmip6-specializations-landice'
	'cmip6-specializations-landsurface'
	'cmip6-specializations-ocean'
	'cmip6-specializations-oceanbgc'
	'cmip6-specializations-seaice'
	'cmip6-specializations-toplevel'
	'esdoc-api'
	'esdoc-archive'
	'esdoc-cdf2cim'
	'esdoc-cdf2cim-ws'
	'esdoc-cim'
	'esdoc-cim-v1-schema'
	'esdoc-cim-v2-schema'
	'esdoc-contrib'
	'esdoc-cv'
	'esdoc-docs'
	'esdoc-errata-client'
	'esdoc-errata-fe'
	'esdoc-errata-ws'
	'esdoc-project'
	'esdoc-py-client'
	'esdoc-web-compare'
	'esdoc-web-demo'
	'esdoc-web-plugin'
	'esdoc-web-search'
	'esdoc-web-splash'
	'esdoc-web-static'
	'esdoc-web-view'
	'esdoc-ws-url-rewriter'
)

# Set of git repos considered to be relatively small.
declare -a ESDOC_REPOS_LITE=(
	'cmip6-specializations-aerosols'
	'cmip6-specializations-atmosphere'
	'cmip6-specializations-atmospheric-chemistry'
	'cmip6-specializations-landice'
	'cmip6-specializations-landsurface'
	'cmip6-specializations-ocean'
	'cmip6-specializations-oceanbgc'
	'cmip6-specializations-seaice'
	'cmip6-specializations-toplevel'
	'esdoc-api'
	'esdoc-cdf2cim'
	'esdoc-cdf2cim-ws'
	'esdoc-cim'
	'esdoc-cim-v1-schema'
	'esdoc-cim-v2-schema'
	'esdoc-contrib'
	'esdoc-cv'
	'esdoc-docs'
	'esdoc-errata-client'
	'esdoc-errata-fe'
	'esdoc-errata-ws'
	'esdoc-py-client'
	'esdoc-web-compare'
	'esdoc-web-demo'
	'esdoc-web-plugin'
	'esdoc-web-search'
	'esdoc-web-splash'
	'esdoc-web-static'
	'esdoc-web-view'
	'esdoc-ws-url-rewriter'
)

# Set of virtual environments.
declare -a ESDOC_VENVS=(
	'api'
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
