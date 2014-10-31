#!/bin/bash

# ###############################################################
# SECTION: HELPER FUNCTIONS
# ###############################################################

# Activates a virtual environment.
activate_venv()
{
	if [ $1 = "api" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_PYESDOC_SRC
		export PYTHONPATH=$PYTHONPATH:$DIR_API_SRC
		export PYTHONPATH=$PYTHONPATH:$DIR_API_TESTS

	elif [ $1 = "qtn" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_QTN_SRC

	elif [ $1 = "mp" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_MP_SRC
		export PYTHONPATH=$PYTHONPATH:$DIR_MP_TESTS

	elif [ $1 = "pyesdoc" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_PYESDOC
		export PYTHONPATH=$PYTHONPATH:$DIR_PYESDOC_SRC
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
		cd $DIR
	fi
}

# Removes all files of passed type in current working directory.
remove_files()
{
	find . -name $1 -exec rm -rf {} \;
}