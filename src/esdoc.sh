#!/bin/bash

BANNER="***************************************************************\n"

# Set paths.
# ... esdoc shell
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR_SHELL="$(dirname "$DIR")"

# ... esdoc shell tmp
DIR_TMP=$DIR_SHELL/tmp

# ... esdoc shell client venv
DIR_PYTHON_VENV_CLIENT=$DIR_SHELL/venv-client

# ... esdoc shell server api venv
DIR_PYTHON_VENV_SERVER_API=$DIR_SHELL/venv-server-api

# ... esdoc shell server questionnaire venv
DIR_PYTHON_VENV_SERVER_QTN=$DIR_SHELL/venv-server-qtn

# ... esdoc root
DIR_ESDOC="$(dirname "$DIR_SHELL")"

# ... esdoc deploy source code
DIR_DEPLOY_SRC=$DIR_ESDOC/esdoc-deploy/src

# ... esdoc api source code
DIR_API_SRC=$DIR_ESDOC/esdoc-api/src

# ... esdoc api tests
DIR_API_TESTS=$DIR_ESDOC/esdoc-api/tests

# ... esdoc api lib sub-folder
DIR_API_LIB="$DIR_API_SRC/esdoc_api/lib"

# ... esdoc mp source code
DIR_MP_SRC=$DIR_ESDOC/esdoc-mp/src

# ... esdoc mp tests
DIR_MP_TESTS=$DIR_ESDOC/esdoc-mp/tests

# ... esdoc py-client source code
DIR_PYESDOC_SRC=$DIR_ESDOC/esdoc-py-client/src

# ... esdoc py-client tests
DIR_PYESDOC_TESTS=$DIR_ESDOC/esdoc-py-client/tests

# ... esdoc py-client source code
DIR_PYESDOC_PYESDOC="$DIR_PYESDOC_SRC/pyesdoc"

# Set action.
ACTION=`echo $1 | tr '[:upper:]' '[:lower:]' | tr '-' '_'`
ACTION_ARG=$2

# Wraps standard echo by adding ES-DOC prefix.
_echo()
{
	if [ "$1" ]; then
	    echo -e "ES-DOC :: $1"	
	else
	    echo -e "ES-DOC ::"	
	fi
}

# Informs user of script configuration.
echo
_echo "# my name -----------------> ${0##*/}"
_echo "# my arguments ------------> ${@}"
_echo "# esdoc root  -------------> $DIR_ESDOC"
_echo "# esdoc shell  ------------> $DIR_SHELL"
_echo "# esdoc venv (client) -----> ${DIR_PYTHON_VENV_CLIENT}"
_echo "# esdoc venv (server-api) -> ${DIR_PYTHON_VENV_SERVER_API}"
_echo "# esdoc tmp ---------------> ${DIR_TMP}"
_echo "# esdoc-api src -----------> ${DIR_API_SRC}"
_echo "# esdoc-api tests ---------> ${DIR_API_TESTS}"
_echo "# esdoc-mp src ------------> ${DIR_MP_SRC}"
_echo "# esdoc-mp tests ----------> ${DIR_MP_TESTS}"
_echo "# esdoc-py-client src -----> ${DIR_MP_SRC}"
_echo "# esdoc-py-client tests ---> ${DIR_MP_TESTS}"
_echo "# action         ----------> ${ACTION}"
echo


# Clears temporary files.
clear_tmp()
{
	rm -rf $DIR_TMP/*
}

# Installs python virtual environments.
_install_python_venv()
{
	rm -rf $1
    mkdir -p $1
    virtualenv -q $1
    source $1/bin/activate
    pip install -r $2    
    deactivate
}

# Installs a git repo.
_install_git_repo()
{
	_echo "... installing git repo :: $1"
	rm -rf $DIR_ESDOC/$1
	git clone https://github.com/ES-DOC/$1.git $DIR_ESDOC/$1
}

# Installs git repos.
install_git_repos()
{
	_echo "Installing git repos"

	_install_git_repo esdoc-api
	_install_git_repo esdoc-cv
	_install_git_repo esdoc-deploy
	_install_git_repo esdoc-docs
	_install_git_repo esdoc-js-client
	_install_git_repo esdoc-mp
	_install_git_repo esdoc-py-client
	_install_git_repo esdoc-questionnaire
	_install_git_repo esdoc-splash
	_install_git_repo esdoc-static
}

# Installs python virtual environments.
install_python_venv()
{
	_echo "Installing virtual environments"

	_echo "... installing server api virtual environment"
	_install_python_venv $DIR_PYTHON_VENV_SERVER_API $DIR/venv-server-api-requirements.txt

	_echo "... installing server questionnaire virtual environment"
	_install_python_venv $DIR_PYTHON_VENV_SERVER_QTN $DIR/venv-server-qtn-requirements.txt

	_echo "... installing client virtual environment"
	_install_python_venv $DIR_PYTHON_VENV_CLIENT $DIR/venv-client-requirements.txt
}

install()
{
	install_git_repos
	install_python_venv
}

activate_python_venv()
{	
	_echo "Activating $1 virtual environment"

	if [ $1 = "api" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_API_SRC
		source $DIR_PYTHON_VENV_SERVER_API/bin/activate

	elif [ $1 = "mp" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_MP_SRC
		export PYTHONPATH=$PYTHONPATH:$DIR_MP_TESTS
		# TODO install nose into client venv
		source $DIR_PYTHON_VENV_SERVER_API/bin/activate
		# source "$DIR_PYTHON_VENV_CLIENT/bin/activate"

	elif [ $1 = "pyesdoc" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_PYESDOC_SRC
		export PYTHONPATH=$PYTHONPATH:$DIR_PYESDOC_TESTS
		# TODO install nose into client venv
		source $DIR_PYTHON_VENV_SERVER_API/bin/activate
		# source "$DIR_PYTHON_VENV_CLIENT/bin/activate"
	fi
}

api_test()
{
	activate_python_venv api

	# All tests.
	if [ ! "$1" ]; then
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

api_visualizer_setup()
{
    _echo "API : writing visualizer setup files ..."

	activate_python_venv api
	python ./esdoc_api_visualizer_setup.py
}

api_misc()
{
    _echo "API : miscellaneous script ..."

	activate_python_venv api
	python ./esdoc_api_misc.py    
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
	cp -r "$DIR_TMP/cim/v1" "$DIR_PYESDOC_PYESDOC/ontologies/cim"

	_echo $BANNER
	_echo "Step 3.  Copying pyesdoc to esdoc_api"
	_echo $BANNER
	cp -r $DIR_PYESDOC_PYESDOC $DIR_API_LIB

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


pyesdoc_test()
{
	activate_python_venv pyesdoc

	# All tests.
	if [ ! "$1" ]; then
	    _echo "pyesdoc :: Executing all pyesdoc tests"
	    nosetests -v -s $DIR_PYESDOC_TESTS/pyesdoc_test

	# Serialization tests.
	elif [ $1 = "s" ]; then
	    _echo "pyesdoc :: Executing pyesdoc serialization tests"
	    nosetests -v -s $DIR_PYESDOC_TESTS/pyesdoc_test/test_serialization.py

	# Publishing tests.
	elif [ $1 = "p" ]; then
	    _echo "pyesdoc :: Executing pyesdoc publishing tests"
	    nosetests -v -s $DIR_PYESDOC_TESTS/pyesdoc_test/test_publishing.py

	# General tests.
	elif [ $1 = "g" ]; then
	    _echo "pyesdoc :: Executing pyesdoc general tests"
	    nosetests -v -s $DIR_PYESDOC_TESTS/pyesdoc_test/test_general.py
	fi
}

pyesdoc_publishing_scenario()
{
	_echo "Executing pyesdoc publishing scenario"

	clear_tmp
	activate_python_venv pyesdoc
	python ./esdoc_pyesdoc_scenario.py
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
	_echo "General commands :"
	_echo "\tinstall-python-venv"
	_echo "\t\tinstall server/client virtual environments"

	_echo ""
	_echo "API commands :"
	_echo "\tapi-test"
	_echo "\t\texecutes api automated tests"
	_echo "\tapi-run"
	_echo "\t\tlaunches api web application"
	_echo "\tapi-db-init"
	_echo "\t\tinitializes database"
	_echo "\tapi-db-ingest"
	_echo "\t\tingests published documents from atom feeds"
	_echo "\tapi-db-ingest-debug"
	_echo "\t\truns ingestion debug script"
	_echo "\tapi-comparator-setup"
	_echo "\t\texecutes comparator setup"
	_echo "\tapi-visualizer-setup"
	_echo "\t\texecutes visualizer setup"
	_echo "\tapi-misc"
	_echo "\t\texecutes miscellaneous script"
	
	_echo ""
	_echo "MP commands :"
	_echo "\tmp-test"
	_echo "\t\texecutes mp automated tests"
	_echo "\tmp-build"
	_echo "\t\tbuilds pyesdoc from meta-programming framework"
	_echo "\tmp-custom-schema"
	_echo "\t\tbuilds custom schema as proof of concept"
	
	_echo ""
	_echo "pyesdoc commands :"
	_echo "\tpyesdoc-test"
	_echo "\t\texecutes pyesdoc automated tests"
	_echo "\tpyesdoc-publishing-scenario"
	_echo "\t\tillustrates pyesdoc usage scenarios"

}

# Invoke action.
$ACTION

exit 0
