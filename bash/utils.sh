#!/bin/bash

# ###############################################################
# SECTION: VARIABLES
# ###############################################################

# Variables.
source $ESDOC_HOME/bash/utils_vars.sh

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
        if [ ! -z "${ESDOC_DIR_TMP}" ]; then
                rm -rf $ESDOC_DIR_TMP/*
                mkdir -p $ESDOC_DIR_TMP
        fi
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
}

# ###############################################################
# SECTION: Initialise file system
# ###############################################################

# Clear temp files.
reset_tmp
