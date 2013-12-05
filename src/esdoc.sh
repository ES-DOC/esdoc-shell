#!/bin/bash

BANNER="***************************************************************\n"

# Set paths.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR_SHELL="$(dirname "$DIR")"
DIR_ESDOC="$(dirname "$DIR_SHELL")"
DIR_TMP=$DIR_SHELL/tmp

DIR_PYTHON_VENV_CLIENT=$DIR_SHELL/venv-client
DIR_PYTHON_VENV_SERVER=$DIR_SHELL/venv-server

DIR_DEPLOY_SRC=$DIR_ESDOC/esdoc-deploy/src

DIR_API_SRC=$DIR_ESDOC/esdoc-api/src
DIR_API_TESTS=$DIR_ESDOC/esdoc-api/tests
DIR_API_LIB="$DIR_API_SRC/esdoc_api/lib"

DIR_MP_SRC=$DIR_ESDOC/esdoc-mp/src
DIR_MP_TESTS=$DIR_ESDOC/esdoc-mp/tests

DIR_PYCLIENT_SRC=$DIR_ESDOC/esdoc-py-client/src
DIR_PYCLIENT_TESTS=$DIR_ESDOC/esdoc-py-client/tests
DIR_PYCLIENT_PYESDOC="$DIR_PYCLIENT_SRC/pyesdoc"

# Set action.
ACTION=$1
ACTION_ARG=$2

_echo()
{
    echo "ES-DOC :: $1"	
}

# Inform user.
echo
_echo "# my name ----------------> ${0##*/}"
_echo "# my arguments -----------> ${@}"
_echo "# esdoc root  ------------> $DIR_ESDOC"
_echo "# esdoc venv (client) ----> ${DIR_PYTHON_VENV_CLIENT}"
_echo "# esdoc venv (server) ----> ${DIR_PYTHON_VENV_SERVER}"
_echo "# esdoc tmp --------------> ${DIR_TMP}"
_echo "# esdoc-api src ----------> ${DIR_API_SRC}"
_echo "# esdoc-api tests --------> ${DIR_API_TESTS}"
_echo "# esdoc-mp src -----------> ${DIR_MP_SRC}"
_echo "# esdoc-mp tests ---------> ${DIR_MP_TESTS}"
_echo "# esdoc-py-client src ----> ${DIR_MP_SRC}"
_echo "# esdoc-py-client tests --> ${DIR_MP_TESTS}"
_echo "# action         ---------> ${ACTION}"
echo



clear_tmp()
{
	rm -rf $DIR_TMP/*
}

activate_python_venv()
{	
	_echo "Activating $1 virtual environment"

	if [ $1 = "api" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_API_SRC
		source $DIR_PYTHON_VENV_SERVER/bin/activate

	elif [ $1 = "mp" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_MP_SRC
		export PYTHONPATH=$PYTHONPATH:$DIR_MP_TESTS
		# TODO install nose into client venv
		source $DIR_PYTHON_VENV_SERVER/bin/activate
		# source "$DIR_PYTHON_VENV_CLIENT/bin/activate"

	elif [ $1 = "pyclient" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_PYCLIENT_SRC
		export PYTHONPATH=$PYTHONPATH:$DIR_PYCLIENT_TESTS
		# TODO install nose into client venv
		source $DIR_PYTHON_VENV_SERVER/bin/activate
		# source "$DIR_PYTHON_VENV_CLIENT/bin/activate"
	fi
}

api_help()
{
	_echo "TODO - api_help"
}

api_test()
{
	activate_python_venv api

	# All tests.
	if [ $1 = "all" ]; then
	    _echo "API :: Executing api tests"
	    nosetests -v -s $DIR_API_TESTS/esdoc_api_test
	fi
}

api_run()
{
    _echo "API : running ..."

	activate_python_venv api
	paster serve --reload $DIR_API_SRC/esdoc_api/config/ini_files/config.ini
}

api_db_init()
{
    _echo "API : initializing db ..."

	# Init app database.
	_echo "API : ... creating db"
	dropdb -h localhost -p 5432 -U postgres -e esdoc_api	
	createdb -h localhost -p 5432 -U postgres -e -O postgres -T template0 esdoc_api

	_echo "API : ... populating db"
	activate_python_venv api
	python ./esdoc_api_db_init.py

	_echo "API : ... creating test db"
	dropdb -h localhost -p 5432 -U postgres -e esdoc_api_test	
	createdb -h localhost -p 5432 -U postgres -e -O postgres -T esdoc_api esdoc_api_test

	_echo "API : created db's"
}

api_db_ingest()
{
    _echo "API : ingesting from external sources ..."

	activate_python_venv api
	python ./esdoc_api_db_ingest.py
}

api_db_ingest_debug()
{
	activate_python_venv api
	python ./esdoc_api_db_ingest_debug.py
}

api_comparator_setup()
{
    _echo "API : writing comparator setup files ..."

	activate_python_venv api
	python ./esdoc_api_comparator_setup.py
}

api_misc()
{
    _echo "API : miscellaneous script ..."

	activate_python_venv api
	python ./esdoc_api_misc.py    
}

mp_help()
{
	_echo "TODO - mp_help"
}

mp_test()
{
	activate_python_venv mp
	# TODO
}

mp_build()
{
    _echo "MP : building ..."

	_echo $BANNER
	_echo "Step 0.  Clearing targets"
	_echo $BANNER
	rm -rf $DIR_TMP"/*"
	# rm -rf $TARGET
	# rm -rf $ESDOC_API

	_echo $BANNER
	_echo "Step 1.  Running es-doc mp utility"
	_echo $BANNER
	activate_python_venv mp	
	python "$DIR_MP_SRC/esdoc_mp" -s "cim" -v "1" -l "python" -o $DIR_TMP

	_echo $BANNER
	_echo "Step 2.  Copying generated files to pyesdoc"
	_echo $BANNER
	cp -r "$DIR_TMP/cim/v1" "$DIR_PYCLIENT_PYESDOC/ontologies/cim"

	_echo $BANNER
	_echo "Step 3.  Copying pyesdoc to esdoc_api"
	_echo $BANNER
	cp -r $DIR_PYCLIENT_PYESDOC $DIR_API_LIB

	_echo $BANNER
	_echo "Step 4.  Cleaning esdoc_api pyesdoc library"
	_echo $BANNER
	find $DIR_API_LIB -type f -name "*.pyc" -exec rm -f {} \;
	find $DIR_API_LIB -type f -name "*.pye" -exec rm -f {} \;
}

mp_custom_schema()
{
	activate_python_venv mp

	python ./esdoc_mp_custom_schema.py $DIR_TMP
}


pyclient_help()
{
	_echo "TODO - pyclient_help"
}

pyclient_test()
{
	activate_python_venv pyclient

	# Serialization tests.
	if [ $1 = "s" ]; then
	    _echo "PYCLIENT :: Executing pyesdoc serialization tests"
	    nosetests -v -s $DIR_PYCLIENT_TESTS/pyesdoc_test/test_serialization.py

	# Publishing tests.
	elif [ $1 = "p" ]; then
	    _echo "PYCLIENT :: Executing pyesdoc publishing tests"
	    nosetests -v -s $DIR_PYCLIENT_TESTS/pyesdoc_test/test_publishing.py

	# General tests.
	elif [ $1 = "g" ]; then
	    _echo "PYCLIENT :: Executing pyesdoc general tests"
	    nosetests -v -s $DIR_PYCLIENT_TESTS/pyesdoc_test/test_general.py

	# All tests.
	elif [ $1 = "all" ]; then
	    _echo "PYCLIENT :: Executing pyesdoc tests"
	    nosetests -v -s $DIR_PYCLIENT_TESTS/pyesdoc_test
	fi
}

pyclient_publishing_scenario()
{
	_echo "Executing pyclient publishing scenario"

	clear_tmp
	activate_python_venv pyclient
	python ./esdoc_pyclient_scenario.py
}

deploy_rollout()
{
	_echo "Rolling out deployment"

	activate_python_venv api
	python "$DIR_DEPLOY_SRC/deploy.py" rollout $DIR_ESDOC test 0.8.6.6 Silence107! Silence107! pEsTuq4d
}

deploy_rollback()
{
	_echo "Rolling back deployment"

	activate_python_venv api
	python "$DIR_DEPLOY_SRC/deploy.py" rollback $DIR_ESDOC test 0.8.6.6 Silence107! Silence107!
}

help()
{
	_echo "api-help"
	_echo "api-test"
	_echo "api-run"
	_echo "api-db-init"
	_echo "api-db-ingest"
	_echo "api-db-ingest-debug"
	_echo "api-comparator-setup"

	_echo "mp-help"
	_echo "mp-test"
	_echo "mp-build"
	_echo "mp-custom-schema"

	_echo "pyclient-help"
	_echo "pyclient-test"
	_echo "pyclient-publishing_scenario"

}


if [ $ACTION = "help" ]; then
	help

# API actions.
elif [ $ACTION = "api-help" ]; then
	api_help
elif [ $ACTION = "api-test" ]; then
	test_api $ACTION_ARG
elif [ $ACTION = "api-run" ]; then
	api_run
elif [ $ACTION = "api-db-init" ]; then
	api_db_init
elif [ $ACTION = "api-db-ingest" ]; then
	api_db_ingest
elif [ $ACTION = "api-db-ingest-debug" ]; then
	api_db_ingest_debug
elif [ $ACTION = "api-misc" ]; then
	api_misc
elif [ $ACTION = "api-comparator-setup" ]; then
	api_comparator_setup

# MP actions.
elif [ $ACTION = "mp-help" ]; then
	mp_help
elif [ $ACTION = "mp-test" ]; then
	mp_test $ACTION_ARG
elif [ $ACTION = "mp-build" ]; then
	mp_build
elif [ $ACTION = "mp-custom-schema" ]; then
	mp_custom_schema

# Pyclient actions.
elif [ $ACTION = "pyclient-help" ]; then
	pyclient_help $ACTION_ARG
elif [ $ACTION = "pyclient-test" ]; then
	pyclient_test $ACTION_ARG
elif [ $ACTION = "pyclient-publishing-scenario" ]; then
	pyclient_publishing_scenario
fi

exit 0
