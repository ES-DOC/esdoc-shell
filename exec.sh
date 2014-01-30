#!/bin/bash

# ###############################################################
# SECTION: INIT 
# ###############################################################

# Set paths.
# ... esdoc root folder
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set path: db.
DIR_DB=$DIR/db

# Set path: repos.
DIR_REPOS=$DIR/repos

# Set path: templates.
DIR_TEMPLATES=$DIR/templates

# Set path: tmp.
DIR_TMP=$DIR/tmp

# Set path: venv.
DIR_VENV=$DIR/venv

# Set path: python.
DIR_PYTHON=$DIR_VENV/python

# Set path: venv pyesdoc
DIR_VENV_PYESDOC=$DIR_VENV/pyesdoc

# Set path: venv meta-programming
DIR_VENV_MP=$DIR_VENV/mp

# Set path: venv api
DIR_VENV_API=$DIR_VENV/api

# Set path: venv questionnaire
DIR_VENV_QTN=$DIR_VENV/questionnaire

# Set path: source code: api
# ... esdoc api source code
DIR_SRC_API=$DIR_REPOS/esdoc-api/src

# Set path: source code: shell
DIR_SRC_SHELL=$DIR_REPOS/esdoc-shell/src

# Set path: source code: deploy
DIR_SRC_DEPLOY=$DIR_REPOS/esdoc-deploy/src

# Set path: source code: meta-programming
DIR_SRC_MP=$DIR_REPOS/esdoc-mp/src

# Set path: source code: pyesdoc
DIR_SRC_PYESDOC=$DIR_REPOS/esdoc-py-client/src

# Set path: source code: questionnaire
DIR_SRC_QTN=$DIR_REPOS/esdoc-questionnaire/src

# Set path: source code: api lib
DIR_LIB_API=$DIR_SRC_API/esdoc_api/lib

# Set path: tests: api
DIR_TESTS_API=$DIR_REPOS/esdoc-api/tests

# Set path: tests: meta-programming
DIR_TESTS_MP=$DIR_REPOS/esdoc-mp/tests

# Set path: tests: pyesdoc
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

_echo_banner()
{
	echo "---------------------------------------------"
}

# Outputs config settings to console.
echo_config()
{
	_echo "CONFIG SETTING: PYTHON_VERSION=$PYTHON_VERSION"
	_echo "CONFIG SETTING: DB_HOSTNAME=$DB_HOSTNAME"
	_echo "CONFIG SETTING: DB_USERNAME=$DB_USERNAME"
	_echo "CONFIG SETTING: DB_SERVER_VERSION=$DB_SERVER_VERSION"
}

# Outputs header information.
_echo_script_header()
{	
	_echo "EXEC PATH: $DIR/exec.sh"
	_echo "EXEC COMMAND: ${1}"
	if [ "$2" ]; then
		_echo "EXEC COMMAND OPTION: ${2}"
	fi
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
# SECTION: BOOTSTRAP
# ###############################################################

# Intiializes configuration files.
_boostrap_init_config()
{
	_echo "... initializing configuration"

	cp $DIR_TEMPLATES/template-config.json $DIR/config.json
	cp $DIR_TEMPLATES/template-exec.config $DIR/exec.config
}

# Displays information notice upon installation.
_bootstrap_notice()
{
	_echo_banner
	_echo "IMPORTANT NOTICE"
	_echo "The bootstrap process installs config files:" 1
	_echo "./esdoc/config.json" 2
	_echo "./esdoc/exec.config" 2
	_echo "Please review and assign settings as appropriate to your " 1
	_echo "environemt prior to continuing with the installation process." 1
	_echo "IMPORTANT NOTICE ENDS"
}

bootstrap()
{
	_echo "BOOTSTRAP STARTS"
	_set_working_dir 
	_boostrap_init_config
	_echo "BOOTSTRAP ENDS"
	_bootstrap_notice
}


# ###############################################################
# SECTION: INSTALL
# ###############################################################

# Installs virtual environments.
_install_venv()
{
	if [ "$2" ]; then
		_echo "... installing virtual environment: "$1" (takes approx 1 minute)"
	fi

	TARGET_VENV=$DIR_VENV/$1	
	TARGET_REQUIREMENTS=$DIR_TEMPLATES/template-venv-$1.txt
	rm -rf $TARGET_VENV
    mkdir -p $TARGET_VENV
    virtualenv -q $TARGET_VENV
    source $TARGET_VENV/bin/activate
    pip install -q --allow-all-external -r $TARGET_REQUIREMENTS 
    deactivate
}

# Installs virtual environments.
_install_venvs()
{
	_install_venv "api" "echo"
	_install_venv "questionnaire" "echo"
	_install_venv "pyesdoc" "echo"
	_install_venv "mp" "echo"
}

# Installs a python executable primed with setuptools, pip & virtualenv.
_install_python()
{
	_echo "... installing python "$PYTHON_VERSION" (takes approx 3 minutes)"

	# Download source.
	_set_working_dir $DIR_PYTHON
	mkdir src	
	cd src
	wget http://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz >/dev/null 2>&1
	tar -xvf Python-$PYTHON_VERSION.tgz >/dev/null 2>&1
	rm Python-$PYTHON_VERSION.tgz

	# Compile.
	cd Python-$PYTHON_VERSION
	./configure --prefix=$DIR_PYTHON >/dev/null 2>&1
	make >/dev/null 2>&1
	make install >/dev/null 2>&1
	export PATH=$DIR_PYTHON/bin:$PATH

	# Install setuptools.
	cd $DIR_PYTHON/src
	wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py >/dev/null 2>&1
	python ez_setup.py >/dev/null 2>&1

	# Install pip.
	easy_install --prefix $DIR_PYTHON pip >/dev/null 2>&1

	# Install virtualenv.
	pip install virtualenv >/dev/null 2>&1
}

# Installs a git repo.
_install_repo()
{
	_echo "... installing repo :: $1"

	rm -rf $DIR_REPOS/$1
	git clone -q https://github.com/ES-DOC/$1.git $DIR_REPOS/$1
}

# Installs git repos.
_install_repos()
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
	_install_repo esdoc-splash
	_install_repo esdoc-static
}

# Sets up directories.
_install_dirs()
{
	mkdir -p $DIR_REPOS
	mkdir -p $DIR_DB/backups
	mkdir -p $DIR_PYTHON
	mkdir -p $DIR_TMP
}

# Installs stack.
install()
{
	_echo "INSTALLING STACK"

	_install_dirs
	_install_repos
	_install_python
	_install_venvs
	_reset_tmp	

	_echo "INSTALLED STACK"
}

# ###############################################################
# SECTION: UPDATE
# ###############################################################

# Displays information notice upon update.
_update_notice()
{
	_echo_banner
	_echo "IMPORTANT NOTICE"
	_echo "The update process created new config files:" 1
	_echo "./esdoc/config.json" 2
	_echo "./esdoc/exec.config" 2
	_echo "It also created a backup of your old config files:" 1
	_echo "./esdoc/config.json-backup" 2
	_echo "./esdoc/exec.config-backup" 2
	_echo "Please verify your local configuration settings accordingly." 1
	_echo "IMPORTANT NOTICE ENDS"
}

_update_venv()
{
	_echo "... updating virtual environment :: $1"

	_uninstall_venv $1
	_install_venv $1
}

# updates virtual environments.
_update_venvs()
{
	export PATH=$DIR_PYTHON/bin:$PATH

	_update_venv "api"
	_update_venv "questionnaire"
	_update_venv "pyesdoc"
	_update_venv "mp"
}

# Updates a repo.
_update_repo()
{
	_echo "... updating repo: $1"

	_set_working_dir $DIR_REPOS/$1
	git pull -q 
	_set_working_dir
}

# Updates repos.
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

# Updates config file.
_update_config()
{
	_echo "... updating configuration"

	cp ./exec.config ./exec.config-backup
	cp ./config.json ./config.json-backup	
	cp $DIR_TEMPLATES/template-config.json $DIR/config.json
	cp $DIR_TEMPLATES/template-exec.config $DIR/exec.config
}

# Updates shell.
_update_shell()
{
	_echo "... updating shell"

	_set_working_dir		
	git pull -q 
}

# Updates stack.
update()
{
	_echo "UPDATING STACK"

	_update_shell
	_update_config
	_update_repos
	_update_venvs	

	_echo "UPDATED STACK"

	_update_notice
}

# ###############################################################
# SECTION: UNINSTALL
# ###############################################################

# Uninstalls shell.
_uninstall_shell()
{
	_echo "... uninstalling shell"

	rm -rf $DIR
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
	_uninstall_repo esdoc-js-clients
	_uninstall_repo esdoc-mp
	_uninstall_repo esdoc-py-client
	_uninstall_repo esdoc-questionnaire
	_uninstall_repo esdoc-splash
	_uninstall_repo esdoc-static
}

# Uninstalls python.
_uninstall_python()
{
	_echo "... uninstalling python"

	rm -rf $DIR_PYTHON
}

# Uninstalls a virtual environment.
_uninstall_venv()
{
	if [ "$2" ]; then
		_echo "... uninstalling virtual environment :: $1"
	fi

	rm -rf $DIR_VENV/$1
}

# Uninstalls virtual environments.
_uninstall_venvs()
{
	_uninstall_venv "api" "echo"
	_uninstall_venv "mp" "echo"
	_uninstall_venv "pyesdoc" "echo"
	_uninstall_venv "questionnaire" "echo"
}

# Uninstalls stack.
uninstall()
{
	_echo "UNINSTALLING STACK"

	_uninstall_venvs
	_uninstall_python
	_uninstall_repos
	_uninstall_shell

	_echo "UNINSTALLED STACK"
}


# ###############################################################
# SECTION: DB FUNCTIONS
# ###############################################################



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

# Load config.
if [ -a $DIR/exec.config ]; then
	_echo_banner
	_echo "Loading config @ ./exec.config"
	source $DIR/exec.config

	# ... set default db host name.
	if [ ! $DB_HOSTNAME ]; then
		DB_HOSTNAME="localhost"
	fi;

	# ... set default db user name.
	if [ ! $DB_USERNAME ]; then
		DB_USERNAME="postgres"
	fi;
fi

# Initialise temporary folder.
_reset_tmp

# Echo standard information.
_echo_banner
_echo_script_header $ACTION $ACTION_ARG
_echo_banner

# Invoke action.
$ACTION $ACTION_ARG

# End.
_echo_banner
exit 0