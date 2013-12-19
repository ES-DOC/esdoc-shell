#!/bin/bash

# Set paths.
# ... esdoc shell
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR_SHELL="$(dirname "$DIR")"

# ... esdoc shell tmp
DIR_TMP=$DIR_SHELL/tmp

# ... esdoc shell pyesdoc venv
DIR_PYTHON_VENV_PYESDOC=$DIR_SHELL/venv/pyesdoc

# ... esdoc shell meta-prgamming venv
DIR_PYTHON_VENV_MP=$DIR_SHELL/venv/mp

# ... esdoc shell api venv
DIR_PYTHON_VENV_SERVER_API=$DIR_SHELL/venv/api

# ... esdoc shell questionnaire venv
DIR_PYTHON_VENV_SERVER_QTN=$DIR_SHELL/venv/questionnaire

# ... esdoc root
DIR_ESDOC="$(dirname "$DIR_SHELL")"

# ... esdoc deploy source code
DIR_DEPLOY_SRC=$DIR_ESDOC/esdoc-deploy/src

# ... esdoc questionnaire source code
DIR_QTN_SRC=$DIR_ESDOC/esdoc-questionnaire/src

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

# Assigns the current working directory.
_set_working_dir()
{
	if [ "$1" ]; then
		cd $1
	else
		cd $DIR
	fi
}

# Wraps standard echo by adding ES-DOC prefix.
_echo()
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

# Resets temporary folder.
_reset_tmp()
{
	rm -rf $DIR_TMP/*
	mkdir -p $DIR_TMP
}

# Installs python virtual environments.
_install_python_venv()
{
	rm -rf $1
    mkdir -p $1
    virtualenv -q $1
    source $1/bin/activate
    pip install -q --allow-all-external -r $2    
    deactivate
}

# Installs a git repo.
_install_git_repo()
{
	_echo "... installing git repo :: $1"

	rm -rf $DIR_ESDOC/$1
	git clone -q https://github.com/ES-DOC/$1.git $DIR_ESDOC/$1
}

# Installs git repos.
install_git_repos()
{
	_echo "Installing git repos:"

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

# Updates a git repo.
_update_git_repo()
{
	_echo "... updating git repo :: $1"

	_set_working_dir $DIR_ESDOC/$1
	git pull -q https://github.com/ES-DOC/$1.git
	_set_working_dir
}

# updates git repos.
update_git_repos()
{
	_echo "Installing git repos:"

	_update_git_repo esdoc-api
	_update_git_repo esdoc-cv
	_update_git_repo esdoc-deploy
	_update_git_repo esdoc-docs
	_update_git_repo esdoc-js-client
	_update_git_repo esdoc-mp
	_update_git_repo esdoc-py-client
	_update_git_repo esdoc-questionnaire
	_update_git_repo esdoc-splash
	_update_git_repo esdoc-static
}

# Installs python virtual environments.
install_python_venv()
{
	_echo "Installing python virtual environments"

	_echo "... installing python virtual environment :: api "
	_install_python_venv $DIR_PYTHON_VENV_SERVER_API $DIR/venv-requirements-api.txt

	_echo "... installing python virtual environment :: questionnaire"
	_install_python_venv $DIR_PYTHON_VENV_SERVER_QTN $DIR/venv-requirements-questionnaire.txt

	_echo "... installing python virtual environment :: pyesdoc"
	_install_python_venv $DIR_PYTHON_VENV_PYESDOC $DIR/venv-requirements-pyesdoc.txt

	_echo "... installing python virtual environment :: meta-programming tools"
	_install_python_venv $DIR_PYTHON_VENV_MP $DIR/venv-requirements-mp.txt

	_echo "Installed python virtual environments"
}

# Deletes python virtual environments.
delete_python_venv()
{
	_echo "Deleting python virtual environments"

	_echo "... deleting python virtual environment :: api "
	rm -rf $DIR_PYTHON_VENV_SERVER_API

	_echo "... deleting python virtual environment :: questionnaire"
	rm -rf $DIR_PYTHON_VENV_SERVER_QTN

	_echo "... deleting python virtual environment :: pyesdoc"
	rm -rf $DIR_PYTHON_VENV_PYESDOC

	_echo "... deleting python virtual environment :: meta-programming tools"
	rm -rf $DIR_PYTHON_VENV_MP

	_echo "Deleted python virtual environments"
}

# Installs configuration files.
install_config()
{
	_echo "Installing configuration files"

	cp ./config-template.json ./config.json	
}

# Installs stack.
install()
{
	install_git_repos
	install_python_venv
	install_config $1
}

# Activates a python virtual environment.
activate_python_venv()
{	
	_echo "Activating $1 virtual environment"

	if [ $1 = "api" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_API_SRC
		source $DIR_PYTHON_VENV_SERVER_API/bin/activate

	elif [ $1 = "qtn" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_QTN_SRC
		source "$DIR_PYTHON_VENV_SERVER_QTN/bin/activate"

	elif [ $1 = "mp" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_MP_SRC
		export PYTHONPATH=$PYTHONPATH:$DIR_MP_TESTS
		source "$DIR_PYTHON_VENV_MP/bin/activate"

	elif [ $1 = "pyesdoc" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_PYESDOC_SRC
		export PYTHONPATH=$PYTHONPATH:$DIR_PYESDOC_TESTS
		source "$DIR_PYTHON_VENV_PYESDOC/bin/activate"
	fi
}

# Executes api tests.
api_test()
{
	activate_python_venv api

	# All tests.
	if [ ! "$1" ]; then
	    _echo "API :: Executing api tests"
	    nosetests -v -s $DIR_API_TESTS/esdoc_api_test
	fi
}

# Launches api web-service.
api_run()
{
    _echo "API : running ..."

	activate_python_venv api
	paster serve --reload $DIR_API_SRC/esdoc_api/config/ini_files/config.ini
}

# Initialises api db.
api_db_init()
{
    _echo "API : DB initializing ..."

    # Drop previous db.
    api_db_delete

	# Init db.
	_echo "API : DB creating"
	createdb -h localhost -p 5432 -U postgres -O postgres -T template0 esdoc_api

	# Seed db.
	_echo "API : DB populating"
	activate_python_venv api
	python ./esdoc.py "api-db-init"

	# Init test db.
	_echo "API : DB creating test db"
	createdb -h localhost -p 5432 -U postgres -O postgres -T esdoc_api esdoc_api_test

	_echo "API : DB initialized"
}

# Deletes existing api db.
api_db_delete()
{
    _echo "API : DB deleting ..."

    # Drop previous db's.
	_echo "API : DB dropping db"
	dropdb -h localhost -p 5432 -U postgres esdoc_api	
	_echo "API : DB dropping test db"
	dropdb -h localhost -p 5432 -U postgres esdoc_api_test	

	_echo "API : DB deleted"
}

# Restores api db from deplyoyment backup file.
api_db_restore()
{
    _echo "API : DB : restoring ..."

	_echo "API : DB dropping existing"
	dropdb -h localhost -p 5432 -U postgres esdoc_api	

	_echo "API : DB creating new"
	createdb -h localhost -p 5432 -U postgres -O postgres -T template0 esdoc_api	

	_echo "API : DB restoring"
	unzip -q $DIR_DEPLOY_SRC/db/db.zip -d $DIR_TMP
	pg_restore -U postgres -d esdoc_api $DIR_TMP/db

	_reset_tmp

    _echo "API : DB : restored"
}

# Launches api db ingestion job.
api_db_ingest()
{
    _echo "API : DB : ingesting from external sources ..."

	activate_python_venv api
	python ./esdoc.py "api-db-ingest"
}

# Launches api db ingestion debug script.
api_db_ingest_debug()
{
    _echo "API : DB : running ingestion debug ..."

	activate_python_venv api
	python ./esdoc_api_db_ingest_debug.py
}

# Executes api comparator setup.
api_comparator_setup()
{
    _echo "API : writing comparator setup files ..."

	activate_python_venv api
	python ./esdoc.py "api-setup-comparators"
}

# Executes api visualizer setup.
api_visualizer_setup()
{
    _echo "API : writing visualizer setup files ..."

	activate_python_venv api
	python ./esdoc.py "api-setup-visualizers"
}

# Executes miscellaneous api script.
api_misc()
{
    _echo "API : miscellaneous script ..."

	activate_python_venv api
	python ./esdoc_api_misc.py    
}

# Executes meta-programming tests.
mp_test()
{
	activate_python_venv mp

    _echo "MP : TODO launch automated tests ..."
}

# Executes meta-programming build process.
mp_build()
{
    _echo "MP : building ..."

	_echo "Step 0.  Resetting"
	_reset_tmp

	_echo "Step 1.  Running es-doc mp utility"
	activate_python_venv mp	
	python "$DIR_MP_SRC/esdoc_mp" -s "cim" -v "1" -l "python" -o $DIR_TMP

	_echo "Step 2.  Copying generated files to pyesdoc"
	cp -r "$DIR_TMP/cim/v1" "$DIR_PYESDOC_PYESDOC/ontologies/cim"

	_echo "Step 3.  Copying generated files to api"
	cp -r $DIR_PYESDOC_PYESDOC $DIR_API_LIB

	_echo "Step 4.  Cleaning"
	find $DIR_API_LIB -type f -name "*.pyc" -exec rm -f {} \;
	find $DIR_API_LIB -type f -name "*.pye" -exec rm -f {} \;
}

# Executes meta-programming build against a custim scheme.
mp_custom_schema()
{
	_reset_tmp
	activate_python_venv mp

	python ./esdoc_exec_mp_scenario.py $DIR_TMP
}

# Executes pyesdoc tests.
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

# Executes pyesdoc publishing scenario.
pyesdoc_publishing_scenario()
{
	_echo "Executing pyesdoc publishing scenario"

	_reset_tmp
	activate_python_venv pyesdoc
	python ./esdoc_exec_pyesdoc_scenario.py $DIR_TMP
}

# Executes deployment rollout.
deploy_rollout()
{
	_echo "Rolling out deployment"

	activate_python_venv api
	python "$DIR_DEPLOY_SRC/deploy.py" rollout $DIR_ESDOC test 0.8.6.6 Silence107! Silence107! pEsTuq4d
}

# Executes deployment rollback.
deploy_rollback()
{
	_echo "Rolling back deployment"

	activate_python_venv api
	python "$DIR_DEPLOY_SRC/deploy.py" rollback $DIR_ESDOC test 0.8.6.6 Silence107! Silence107!
}

# Displays help information to user.
help()
{
	_echo "General commands :"
	_echo "install-python-venv" 1
	_echo "install server/client virtual environments" 2

	_echo ""
	_echo "API commands :"
	_echo "api-test" 1
	_echo "executes api automated tests" 2
	_echo "api-run" 1
	_echo "launches api web application" 2
	_echo "api-db-init" 1
	_echo "initializes database" 2
	_echo "api-db-restore" 1
	_echo "initializes database restore from deployment backup" 2
	_echo "api-db-ingest" 1

	_echo "ingests published documents from atom feeds" 2
	_echo "api-db-ingest-debug" 1
	_echo "runs ingestion debug script" 2
	_echo "api-comparator-setup" 1
	_echo "executes comparator setup" 2
	_echo "api-visualizer-setup" 1
	_echo "executes visualizer setup" 2
	_echo "api-misc" 1
	_echo "executes miscellaneous script" 2
	
	_echo ""
	_echo "MP commands :"
	_echo "mp-test" 1
	_echo "executes mp automated tests" 2
	_echo "mp-build" 1
	_echo "builds pyesdoc from meta-programming framework" 2
	_echo "mp-custom-schema" 1
	_echo "builds custom schema as proof of concept" 2
	
	_echo ""
	_echo "PYESDOC commands :"
	_echo "pyesdoc-test" 1cutes pyesdo
	_echo "exec automated tests" 2
	_echo "pyesdoc-publishing-scenario" 1
	_echo "illustrates pyesdoc usage scenarios" 2
}

# Set working directory.
_set_working_dir

# Invoke action.
$ACTION $ACTION_ARG

exit 0
