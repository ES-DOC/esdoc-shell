#!/bin/bash


# ###############################################################
# SECTION: INIT
# ###############################################################

# Set paths.
# ... esdoc root folder
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# ... esdoc git repos root folder.
DIR_REPOS=$DIR/repos

# ... esdoc tmp folder.
DIR_TMP=$DIR/tmp

# ... esdoc virtual environment folder.
DIR_VENV=$DIR/venv

# ... esdoc webapps root folder.
DIR_WEBAPPS=$DIR/webapps

# ... esdoc shell pyesdoc venv
DIR_VENV_PYESDOC=$DIR_VENV/pyesdoc

# ... esdoc shell meta-prgamming venv
DIR_VENV_MP=$DIR_VENV/mp

# ... esdoc shell api venv
DIR_VENV_API=$DIR_VENV/api

# ... esdoc shell questionnaire venv
DIR_VENV_QTN=$DIR_VENV/questionnaire

# ... esdoc api source code
DIR_SRC_API=$DIR_REPOS/esdoc-api/src

# ... esdoc shell source code
DIR_SRC_SHELL=$DIR_REPOS/esdoc-shell/src

# ... esdoc deploy source code
DIR_SRC_DEPLOY=$DIR_REPOS/esdoc-deploy/src

# ... esdoc mp source code
DIR_SRC_MP=$DIR_REPOS/esdoc-mp/src

# ... esdoc py-client source code
DIR_SRC_PYESDOC=$DIR_REPOS/esdoc-py-client/src

# ... esdoc questionnaire source code
DIR_SRC_QTN=$DIR_REPOS/esdoc-questionnaire/src

# ... esdoc api lib sub-folder
DIR_LIB_API=$DIR_SRC_API/esdoc_api/lib

# ... esdoc api tests
DIR_TESTS_API=$DIR_REPOS/esdoc-api/tests

# ... esdoc mp tests
DIR_TESTS_MP=$DIR_REPOS/esdoc-mp/tests

# ... esdoc py-client tests
DIR_TESTS_PYESDOC=$DIR_REPOS/esdoc-py-client/tests

# Set action.
ACTION=`echo $1 | tr '[:upper:]' '[:lower:]' | tr '-' '_'`

# Set action argument.
ACTION_ARG=$2


# ###############################################################
# SECTION: HELPER FUNCTIONS
# ###############################################################

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

# Outputs working folders.
show_working_folders()
{
	_echo $DIR
	_echo $DIR_REPOS
	_echo $DIR_TMP
	_echo $DIR_WEBAPPS

	_echo $DIR_VENV
	_echo $DIR_VENV_QTN
	_echo $DIR_VENV_API
	_echo $DIR_VENV_MP
	_echo $DIR_VENV_PYESDOC

	_echo $DIR_SRC_DEPLOY
	_echo $DIR_SRC_QTN
	_echo $DIR_SRC_API
	_echo $DIR_TESTS_API
	_echo $DIR_LIB_API
	_echo $DIR_SRC_MP
	_echo $DIR_TESTS_MP
	_echo $DIR_SRC_PYESDOC
	_echo $DIR_TESTS_PYESDOC	
}

# Assigns the current working directory.
_set_working_dir()
{
	if [ "$1" ]; then
		cd $1
	else
		cd $DIR
	fi
}

# Resets temporary folder.
_reset_tmp()
{
	rm -rf $DIR_TMP/*
	mkdir -p $DIR_TMP
}

# Activates a virtual environment.
_activate_venv()
{	
	_echo "Activating $1 virtual environment"

	if [ $1 = "api" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_SRC_API
		_echo $DIR_VENV_API/bin/activate
		source $DIR_VENV_API/bin/activate

	elif [ $1 = "qtn" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_SRC_QTN
		source "$DIR_VENV_QTN/bin/activate"

	elif [ $1 = "mp" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_SRC_MP
		export PYTHONPATH=$PYTHONPATH:$DIR_TESTS_MP
		source "$DIR_VENV_MP/bin/activate"

	elif [ $1 = "pyesdoc" ]; then
		export PYTHONPATH=$PYTHONPATH:$DIR_SRC_PYESDOC
		export PYTHONPATH=$PYTHONPATH:$DIR_TESTS_PYESDOC
		source "$DIR_VENV_PYESDOC/bin/activate"
	fi
}

# ###############################################################
# SECTION: SETUP FUNCTIONS
# ###############################################################

# Installs a git repo.
_install_repo()
{
	_echo "... installing repo :: $1"

	rm -rf $DIR_REPOS/$1
	git clone -q https://github.com/ES-DOC/$1.git $DIR_REPOS/$1
}

# Installs git repos.
install_repos()
{
	_install_repo esdoc-api
	_install_repo esdoc-bootstrap
	_install_repo esdoc-cv
	_install_repo esdoc-deploy
	_install_repo esdoc-docs
	_install_repo esdoc-js-client
	_install_repo esdoc-mp
	_install_repo esdoc-py-client
	_install_repo esdoc-questionnaire
	_install_repo esdoc-shell
	_install_repo esdoc-splash
	_install_repo esdoc-static
}

# Installs virtual environment.
_install_venv()
{
	rm -rf $1
    mkdir -p $1
    virtualenv -q $1
    source $1/bin/activate
    pip install -q --allow-all-external -r $2    
    deactivate
}

# Installs virtual environments.
install_venvs()
{
	_echo "... installing virtual environment :: api "
	_install_venv $DIR_VENV_API $DIR_SRC_SHELL/venv-requirements-api.txt

	_echo "... installing virtual environment :: questionnaire"
	_install_venv $DIR_VENV_QTN $DIR_SRC_SHELL/venv-requirements-questionnaire.txt

	_echo "... installing virtual environment :: pyesdoc"
	_install_venv $DIR_VENV_PYESDOC $DIR_SRC_SHELL/venv-requirements-pyesdoc.txt

	_echo "... installing virtual environment :: mp"
	_install_venv $DIR_VENV_MP $DIR_SRC_SHELL/venv-requirements-mp.txt
}

# Installs configuration files.
install_config()
{
	_echo "... installing configuration file"

	cp ./repos/esdoc-shell/src/config.json ./config.json	
}

# Displays information notice upon update.
_display_install_notice()
{
	_echo "IMPORTANT NOTICE"
	_echo "The install process installs a config file @ ./esdoc/config.json." 1
	_echo "Please review and assign configuration settings as appropriate to your environemt." 1
	_echo "IMPORTANT NOTICE ENDS"
}

# Installs stack.
install()
{
	_echo "INSTALLING STACK"

	install_repos
	install_venvs
	install_config

	_echo "INSTALLED STACK"

	_display_install_notice
}

# Updates a git repo.
_update_repo()
{
	_echo "... updating repo :: $1"

	_set_working_dir $DIR_REPOS/$1
	git pull -q https://github.com/ES-DOC/$1.git
	_set_working_dir
}

# updates git repos.
_update_repos()
{
	_update_repo esdoc-api
	_update_repo esdoc-bootstrap
	_update_repo esdoc-cv
	_update_repo esdoc-deploy
	_update_repo esdoc-docs
	_update_repo esdoc-js-client
	_update_repo esdoc-mp
	_update_repo esdoc-py-client
	_update_repo esdoc-questionnaire
	_update_repo esdoc-splash
	_update_repo esdoc-static
}

# updates virtual environments.
_update_venvs()
{
	_echo "... updating virtual environment :: api "
	_uninstall_venv $DIR_VENV_API
	_install_venv $DIR_VENV_API $DIR_SRC_SHELL/venv-requirements-api.txt

	_echo "... updating virtual environment :: questionnaire"
	_uninstall_venv $DIR_VENV_QTN
	_install_venv $DIR_VENV_QTN $DIR_SRC_SHELL/venv-requirements-questionnaire.txt

	_echo "... updating virtual environment :: pyesdoc"
	_uninstall_venv $DIR_VENV_PYESDOC
	_install_venv $DIR_VENV_PYESDOC $DIR_SRC_SHELL/venv-requirements-pyesdoc.txt

	_echo "... updating virtual environment :: mp"
	_uninstall_venv $DIR_VENV_MP
	_install_venv $DIR_VENV_MP $DIR_SRC_SHELL/venv-requirements-mp.txt
}

# Updates config file.
_update_config()
{
	_echo "... updating configuration file"

	cp ./config.json ./config-backup.json	
	cp ./repos/esdoc-shell/src/config.json ./config.json	
}

# Updates shell script.
_update_shell_script()
{
	_echo "... updating shell script"

	cp ./repos/esdoc-shell/src/exec.sh ./exec.sh
}

# Displays information notice upon update.
_display_update_notice()
{
	_echo "IMPORTANT NOTICE"
	_echo "The update process created a new config file @ ./esdoc/config.json." 1
	_echo "It also created a backup of your old config file @ ./esdoc/config-backup.json" 1
	_echo "Please reset your configuration settings accordingly." 1
	_echo "IMPORTANT NOTICE ENDS"
}


# Updates stack.
update()
{
	_echo "UPDATING STACK"

	_update_repos
	_update_venvs	
	_update_shell_script
	_update_config

	_echo "UPDATED STACK"

	_display_update_notice
}

# Uninstalls virtual environments.
_uninstall_venv()
{
	rm -rf $1
}

# Uninstalls virtual environments.
_uninstall_venvs()
{
	_echo "... uninstalling virtual environment :: api "
	_uninstall_venv $DIR_VENV_API

	_echo "... uninstalling virtual environment :: questionnaire"
	_uninstall_venv $DIR_VENV_QTN

	_echo "... uninstalling virtual environment :: pyesdoc"
	_uninstall_venv $DIR_VENV_PYESDOC

	_echo "... uninstalling virtual environment :: mp"
	_uninstall_venv $DIR_VENV_MP
}

# Uninstalls git repo.
_uninstall_repo()
{
	rm -rf $DIR_REPOS/$1
}

# Uninstalls git repos.
_uninstall_repos()
{
	_echo "... uninstalling repos"

	_uninstall_repo esdoc-api
	_uninstall_repo esdoc-bootstrap
	_uninstall_repo esdoc-cv
	_uninstall_repo esdoc-deploy
	_uninstall_repo esdoc-docs
	_uninstall_repo esdoc-js-client
	_uninstall_repo esdoc-mp
	_uninstall_repo esdoc-py-client
	_uninstall_repo esdoc-questionnaire
	_uninstall_repo esdoc-splash
	_uninstall_repo esdoc-static
}

# Uninstalls stack.
uninstall()
{
	_echo "UNINSTALLING STACK ..."

	_uninstall_repos
	_uninstall_venvs
	_reset_tmp
	cd ..
	rm -rf esdoc

	_echo "UNINSTALLED STACK"
}

# ###############################################################
# SECTION: API FUNCTIONS
# ###############################################################

# Executes api tests.
api_test()
{
	_activate_venv api

	# All tests.
	if [ ! "$1" ]; then
	    _echo "API :: Executing api tests"
	    nosetests -v -s $DIR_TESTS_API/esdoc_api_test
	fi
}

# Launches api web-service.
api_run()
{
    _echo "API : running ..."

	_activate_venv api
	paster serve --reload $DIR_SRC_API/esdoc_api/config/ini_files/config.ini
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
	_activate_venv api
	python ./exec.py "api-db-init"

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
	unzip -q $DIR_SRC_DEPLOY/db/db.zip -d $DIR_TMP
	pg_restore -U postgres -d esdoc_api $DIR_TMP/db

	_reset_tmp

    _echo "API : DB : restored"
}

# Launches api db ingestion job.
api_db_ingest()
{
    _echo "API : DB : ingesting from external sources ..."

	_activate_venv api
	python ./exec.py "api-db-ingest"
}

# Executes api comparator setup.
api_comparator_setup()
{
    _echo "API : writing comparator setup files ..."

	_activate_venv api
	python ./exec.py "api-setup-comparators"
}

# Executes api visualizer setup.
api_visualizer_setup()
{
    _echo "API : writing visualizer setup files ..."

	_activate_venv api
	python ./exec.py "api-setup-visualizers"
}


# ###############################################################
# SECTION: META-PROGRAMMING FUNCTIONS
# ###############################################################

# Executes meta-programming tests.
mp_test()
{
	_activate_venv mp

    _echo "MP : TODO launch automated tests ..."
}

# Executes meta-programming build process.
mp_build()
{
    _echo "MP : building ..."
	show_working_folders    

	_echo "Step 0.  Resetting"
	_reset_tmp

	_echo "Step 1.  Running es-doc mp utility"
	_activate_venv mp	
	python "$DIR_SRC_MP/esdoc_mp" -s "cim" -v "1" -l "python" -o $DIR_TMP

	_echo "Step 2.  Copying generated files to pyesdoc"
	cp -r "$DIR_TMP/cim/v1" "$DIR_SRC_PYESDOC/pyesdoc/ontologies/cim"

	_echo "Step 3.  Copying generated files to api"
	cp -r $DIR_SRC_PYESDOC/pyesdoc $DIR_LIB_API

	_echo "Step 4.  Cleaning"
	find $DIR_SRC_PYESDOC -type f -name "*.pyc" -exec rm -f {} \;
	find $DIR_SRC_PYESDOC -type f -name "*.pye" -exec rm -f {} \;
	find $DIR_LIB_API -type f -name "*.pyc" -exec rm -f {} \;
	find $DIR_LIB_API -type f -name "*.pye" -exec rm -f {} \;
}

# Executes meta-programming build against a custim scheme.
mp_custom_schema()
{
	_reset_tmp
	_activate_venv mp

	python ./exec_mp_scenario.py $DIR_TMP
}


# ###############################################################
# SECTION: PYESDOC FUNCTIONS
# ###############################################################

# Executes pyesdoc tests.
pyesdoc_test()
{
	_activate_venv pyesdoc

	# All tests.
	if [ ! "$1" ]; then
	    _echo "pyesdoc :: Executing all pyesdoc tests"
	    nosetests -v -s $DIR_TESTS_PYESDOC/pyesdoc_test

	# Serialization tests.
	elif [ $1 = "s" ]; then
	    _echo "pyesdoc :: Executing pyesdoc serialization tests"
	    nosetests -v -s $DIR_TESTS_PYESDOC/pyesdoc_test/test_serialization.py

	# Publishing tests.
	elif [ $1 = "p" ]; then
	    _echo "pyesdoc :: Executing pyesdoc publishing tests"
	    nosetests -v -s $DIR_TESTS_PYESDOC/pyesdoc_test/test_publishing.py

	# General tests.
	elif [ $1 = "g" ]; then
	    _echo "pyesdoc :: Executing pyesdoc general tests"
	    nosetests -v -s $DIR_TESTS_PYESDOC/pyesdoc_test/test_general.py
	fi
}

# Executes pyesdoc publishing scenario.
pyesdoc_publishing_scenario()
{
	_echo "Executing pyesdoc publishing scenario"

	_reset_tmp
	_activate_venv pyesdoc
	python ./exec_pyesdoc_scenario.py $DIR_TMP
}

# Executes miscellaneous script.
misc()
{
    _echo "OTHER : miscellaneous script ..."

	_activate_venv pyesdoc
	python ./exec_misc_scenario.py    
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

	_echo ""
	_echo "misc" 1
	_echo "executes miscellaneous script" 2	
}

# ###############################################################
# SECTION: MAIN
# ###############################################################

# Initialise working directory.
_set_working_dir

# Initialise temporary folder.
_reset_tmp

# Display header.
# _show_script_header $ACTION $ACTION_ARG

# Invoke action.
$ACTION $ACTION_ARG

exit 0
