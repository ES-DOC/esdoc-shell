#!/bin/bash

# ###############################################################
# SECTION: HELPER FUNCTIONS
# ###############################################################

# Activates a virtual environment.
activate_venv()
{
	export PYTHONPATH=$ESDOC_DIR_BASH:$PYTHONPATH
	venv_path=$ESDOC_SHELL_VENV
	source $venv_path/bin/activate
	log "venv activated @ "$venv_path
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
	source $ESDOC_HOME/repos/core/esdoc-api/sh/activate
	source $ESDOC_HOME/repos/core/esdoc-archive/sh/activate
	source $ESDOC_HOME/repos/core/esdoc-py-client/sh/activate
	source $ESDOC_HOME/repos/core/esdoc-cdf2cim/sh/activate
	source $ESDOC_HOME/repos/core/esdoc-cdf2cim-ws/sh/activate
	source $ESDOC_HOME/repos/core/esdoc-errata-ws/sh/activate
	source $ESDOC_HOME/repos/core/esdoc-web-plugin/sh/activate
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
declare ESDOC_DIR_REPOS_EXT=$ESDOC_DIR_REPOS/ext
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
	'https://github.com/ES-DOC/esdoc-api.git'
	'https://github.com/ES-DOC/esdoc-cdf2cim.git'
	'https://github.com/ES-DOC/esdoc-cdf2cim-archive.git'
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
	'https://github.com/ES-DOC/esdoc-web-demo.git'
	'https://github.com/ES-DOC/esdoc-web-plugin.git'
	'https://github.com/ES-DOC/esdoc-web-search.git'
	'https://github.com/ES-DOC/esdoc-web-static.git'
	'https://github.com/ES-DOC/esdoc-web-view.git'
	'https://github.com/ES-DOC/esdoc-web-view-furtherinfo.git'
	'https://github.com/ES-DOC/esdoc-web-view-specialization.git'
	'https://github.com/ES-DOC/esdoc-ws-url-rewriter.git'
	'https://github.com/ES-DOC/pyessv.git'
	'https://github.com/ES-DOC/pyessv-archive.git'
	'https://github.com/ES-DOC/pyessv-js.git'
)

# Set of cmip6 git repos.
declare -a ESDOC_REPOS_CMIP6=(
	'https://github.com/ES-DOC/cmip6-dashboard.git'
	'https://github.com/ES-DOC/cmip6-specializations-toplevel.git'
	'https://github.com/ES-DOC/cmip6-specializations-seaice.git'
	'https://github.com/ES-DOC/cmip6-specializations-ocnbgchem.git'
	'https://github.com/ES-DOC/cmip6-specializations-ocean.git'
	'https://github.com/ES-DOC/cmip6-specializations-landice.git'
	'https://github.com/ES-DOC/cmip6-specializations-land.git'
	'https://github.com/ES-DOC/cmip6-specializations-atmoschem.git'
	'https://github.com/ES-DOC/cmip6-specializations-atmos.git'
	'https://github.com/ES-DOC/cmip6-specializations-aerosol.git'
)

# Set of external git repos.
declare -a ESDOC_REPOS_EXT=(
	'https://github.com/ESGF/esgf-config.git'
	'https://github.com/ESGF/esgf-prepare.git'
	'https://github.com/WCRP-CMIP/CMIP6_CVs.git'
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
