#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Installs virtual environments.
_install_venv()
{
	if [ "$2" ]; then
		log "Installing virtual environment: $1"
	fi

	# Make directory.
	declare TARGET_VENV=$ESDOC_DIR_VENV/$1
	rm -rf $TARGET_VENV
    mkdir -p $TARGET_VENV

    # Initialise venv.
    export PATH=$ESDOC_DIR_PYTHON/bin:$PATH
	export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_PYTHON
    virtualenv -q $TARGET_VENV

    # Build dependencies.
    source $TARGET_VENV/bin/activate
	declare TARGET_REQUIREMENTS=$ESDOC_DIR_RESOURCE/venv/venv-requirements-$1.txt
    pip install -q --allow-all-external -r $TARGET_REQUIREMENTS

    # Cleanup.
    deactivate
}

# Installs python virtual environments.
_install_venvs()
{
	for venv in "${ESDOC_VENVS[@]}"
	do
		_install_venv $venv "echo"
	done
}

# Installs a python executable primed with setuptools, pip & virtualenv.
_install_python_executable()
{
	# Version of python used by stack.
	declare PYTHON_VERSION=2.7.10

	log "Installing python "$PYTHON_VERSION" (takes approx 2 minutes)"

	# Download source.
	set_working_dir $ESDOC_DIR_PYTHON
	mkdir src
	cd src
	wget http://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz --no-check-certificate
	tar -xvf Python-$PYTHON_VERSION.tgz
	rm Python-$PYTHON_VERSION.tgz

	# Compile.
	cd Python-$PYTHON_VERSION
	./configure --prefix=$ESDOC_DIR_PYTHON
	make
	make install
	export PATH=$ESDOC_DIR_PYTHON/bin:$PATH
	export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_PYTHON

	# Install setuptools.
	cd $ESDOC_DIR_PYTHON/src
	wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
	python ez_setup.py

	# Install pip.
	easy_install --prefix $ESDOC_DIR_PYTHON pip

	# Install virtualenv.
	pip install virtualenv
}

# Installs a git repo.
_install_repo()
{
	log "Installing repo: $1"
	rm -rf $ESDOC_DIR_REPOS/$1
	git clone -q https://github.com/ES-DOC/$1.git $ESDOC_DIR_REPOS/$1
}

# Installs git repos.
_install_repos()
{
	log "Installing repos"
	for repo in "${ESDOC_REPOS[@]}"
	do
		_install_repo $repo
	done
}

# Sets up directories.
_install_dirs()
{
	# new
	for ops_dir in "${ESDOC_OPS_DIRS[@]}"
	do
		mkdir -p $ops_dir
	done
	mkdir -p $ESDOC_DIR_REPOS
	mkdir -p $ESDOC_DIR_PYTHON
}

# Sets up configuration.
_install_configuration()
{
	cp $DIR_RESOURCES/template-user-api.conf $ESDOC_DIR_CONFIG/api.conf
	cp $DIR_RESOURCES/template-user-pyesdoc.conf $ESDOC_DIR_CONFIG/pyesdoc.conf
	cp $DIR_RESOURCES/template-user-api-supervisord.conf $ESDOC_DIR_DAEMONS/api/supervisord.conf
}

# Sets up script permissions.
_install_script_permissions()
{
	chmod a+x $ESDOC_HOME/bash/api/*.sh
	chmod a+x $ESDOC_HOME/bash/archive/*.sh
	chmod a+x $ESDOC_HOME/bash/deployment/*.sh
	chmod a+x $ESDOC_HOME/bash/mp/*.sh
	chmod a+x $ESDOC_HOME/bash/pyesdoc/*.sh
	chmod a+x $ESDOC_HOME/bash/stack/*.sh
}

# Main entry point.
main()
{
	log "INSTALLING STACK"

	_install_dirs
	_install_configuration
	_install_script_permissions
	_install_repos
	_install_python_executable
	_install_venvs

	log "INSTALLED STACK"
}

# Invoke entry point.
main
