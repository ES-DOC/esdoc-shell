#!/bin/bash

# ###############################################################
# SECTION: BOOTSTRAP
# ###############################################################

# Copies configuration templates from resources to ops/config.
_copy_config_templates()
{
	cp $DIR_RESOURCES/user/template-api.conf $DIR_CONFIG/api.conf
	cp $DIR_RESOURCES/user/template-pyesdoc.conf $DIR_CONFIG/pyesdoc.conf
	cp $DIR_RESOURCES/user/template-esdoc.sh $DIR_CONFIG/esdoc.sh
}

# Run stack bootstrapper.
run_stack_bootstrap()
{
	log "BOOTSTRAP STARTS"
	set_working_dir

	log "Creating ops directories"
	mkdir -p $DIR_DEFAULT_ARCHIVE
	mkdir -p $DIR_BACKUPS
	mkdir -p $DIR_CONFIG
	mkdir -p $DIR_DAEMONS
	mkdir -p $DIR_LOGS
	mkdir -p $DIR_PYTHON
	mkdir -p $DIR_TMP
	mkdir -p $DIR_VENV

	log "Initializing configuration"
	_copy_config_templates

	log "BOOTSTRAP ENDS"

	log_banner
	log "IMPORTANT NOTICE"
	log "The bootstrap process installs 3 config files:" 1
	log "$DIR_CONFIG/api.conf" 2
	log "$DIR_CONFIG/pyesdoc.conf" 2
	log "$DIR_CONFIG/esdoc.sh" 2
	log "Please review and assign settings as appropriate to your " 1
	log "environment prior to continuing with the installation process." 1
	log "IMPORTANT NOTICE ENDS"
}

# ###############################################################
# SECTION: INSTALL
# ###############################################################

# Installs virtual environments.
run_install_venv()
{
	if [ "$2" ]; then
		log "Installing virtual environment: $1"
	fi

	# Make directory.
	declare TARGET_VENV=$DIR_VENV/$1
	rm -rf $TARGET_VENV
    mkdir -p $TARGET_VENV

    # Initialise venv.
    export PATH=$DIR_PYTHON/bin:$PATH
    virtualenv -q $TARGET_VENV

    # Build dependencies.
    source $TARGET_VENV/bin/activate
	declare TARGET_REQUIREMENTS=$DIR_RESOURCES/venv/requirements-$1.txt
    pip install -q --allow-all-external -r $TARGET_REQUIREMENTS

    # Cleanup.
    deactivate
}

# Installs python virtual environments.
run_install_venvs()
{
	for venv in "${VENVS[@]}"
	do
		run_install_venv $venv "echo"
	done
}

# Installs a python executable primed with setuptools, pip & virtualenv.
run_install_python()
{
	log "Installing python "$PYTHON_VERSION" (takes approx 3 minutes)"

	# Download source.
	mkdir -p $DIR_PYTHON/src
	set_working_dir $DIR_PYTHON/src
	wget http://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz --no-check-certificate
	tar -xvf Python-$PYTHON_VERSION.tgz
	rm Python-$PYTHON_VERSION.tgz

	# Compile.
	set_working_dir $DIR_PYTHON/src/Python-$PYTHON_VERSION
	./configure --prefix=$DIR_PYTHON
	make
	make install
	export PATH=$DIR_PYTHON/bin:$PATH

	# Install setuptools.
	set_working_dir $DIR_PYTHON/src
	wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
	python ez_setup.py

	# Install pip.
	easy_install --prefix $DIR_PYTHON pip

	# Install virtualenv.
	pip install virtualenv
}

# Installs a git repo.
run_install_repo()
{
	log "Installing repo: $1"

	rm -rf $DIR_REPOS/$1
	git clone -q https://github.com/ES-DOC/$1.git $DIR_REPOS/$1
}

# Installs git repos.
run_install_repos()
{
	for repo in "${REPOS[@]}"
	do
		run_install_repo $repo
	done
}

# Sets up directories.
_install_dirs()
{
	mkdir -p $DIR_LOGS
	mkdir -p $DIR_PYTHON
	mkdir -p $DIR_REPOS
	mkdir -p $DIR_TMP
}

# Installs stack.
run_stack_install()
{
	log "INSTALLING STACK"

	_install_dirs
	run_install_repos
	run_install_python
	run_install_venvs

	log "INSTALLED STACK"
}


# ###############################################################
# SECTION: UPDATE
# ###############################################################

# Display post update notice.
_update_notice()
{
	log_banner
	log "IMPORTANT NOTICE"
	log "The update process created new config files:" 1
	log "$DIR_CONFIG/api.conf" 2
	log "$DIR_CONFIG/pyesdoc.conf" 2
	log "It also created a backup of your old config file:" 1
	log "$DIR_CONFIG/api.conf-backup" 2
	log "$DIR_CONFIG/pyesdoc.conf-backup" 2
	log "Please verify your local configuration settings accordingly." 1
	log "IMPORTANT NOTICE ENDS"
}

# Updates a virtual environment.
run_stack_update_venv()
{
	log "Updating virtual environment :: $1"

	_uninstall_venv $1
	run_install_venv $1
}

# Updates virtual environments.
run_stack_update_venvs()
{
	export PATH=$DIR_PYTHON/bin:$PATH
	for venv in "${VENVS[@]}"
	do
		run_stack_update_venv $venv
	done
}

# Updates a git repo.
run_stack_update_repo()
{
	log "Updating repo: $1"

	set_working_dir $DIR_REPOS/$1
	git pull -q
	remove_files "*.pyc"
	set_working_dir
}

# Updates git repos.
run_stack_update_repos()
{
	for repo in "${REPOS[@]}"
	do
		run_stack_update_repo $repo
	done
}

# Updates configuration.
_update_config()
{
	log "Updating configuration"

	# Create backups.
	cp $DIR_CONFIG/api.conf $DIR_CONFIG/api.conf-backup
	cp $DIR_CONFIG/pyesdoc.conf $DIR_CONFIG/pyesdoc.conf-backup

	# Copy new config.
	_copy_config_templates
}

# Updates shell.
run_stack_update_shell()
{
	log "Updating shell"

	set_working_dir
	git pull -q
	remove_files "*.pyc"
}

# Updates stack.
run_stack_update()
{
	log "UPDATING STACK"

	run_stack_update_shell
	_update_config
	run_stack_update_repos
	run_stack_update_venvs

	log "UPDATED STACK"

	_update_notice
}


# ###############################################################
# SECTION: UNINSTALL
# ###############################################################

# Uninstalls shell.
_uninstall_shell()
{
	log "Uninstalling shell"

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
	log "Uninstalling repos"

	for repo in "${REPOS[@]}"
	do
		_uninstall_repo $repo
	done
}

# Uninstalls python.
_uninstall_python()
{
	log "Uninstalling python"

	rm -rf $DIR_PYTHON
}

# Uninstalls a virtual environment.
_uninstall_venv()
{
	if [ "$2" ]; then
		log "Uninstalling virtual environment :: $1"
	fi

	rm -rf $DIR_VENV/$1
}

# Uninstalls virtual environments.
_uninstall_venvs()
{
	for venv in "${VENVS[@]}"
	do
		_uninstall_venv $venv "echo"
	done
}

# Uninstalls stack.
run_stack_uninstall()
{
	log "UNINSTALLING STACK"

	_uninstall_venvs
	_uninstall_python
	_uninstall_repos
	_uninstall_shell

	log "UNINSTALLED STACK"
}