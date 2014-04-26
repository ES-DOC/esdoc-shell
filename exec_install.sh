# ###############################################################
# SECTION: BOOTSTRAP
# ###############################################################

# Intiializes configuration files.
_boostrap_init_config()
{
	log "... initializing configuration"

	cp $DIR_TEMPLATES/template-config.json $DIR/config.json
	cp $DIR_TEMPLATES/template-exec.config $DIR/exec.config
}

# Displays information notice upon installation.
_bootstrap_notice()
{
	log_banner
	log "IMPORTANT NOTICE"
	log "The bootstrap process installs config files:" 1
	log "./esdoc/config.json" 2
	log "./esdoc/exec.config" 2
	log "Please review and assign settings as appropriate to your " 1
	log "environemt prior to continuing with the installation process." 1
	log "IMPORTANT NOTICE ENDS"
}

run_bootstrap()
{
	log "BOOTSTRAP STARTS"
	set_working_dir
	_boostrap_init_config
	log "BOOTSTRAP ENDS"
	_bootstrap_notice
}


# ###############################################################
# SECTION: INSTALL
# ###############################################################

# Installs virtual environments.
_install_venv()
{
	if [ "$2" ]; then
		log "... installing virtual environment: "$1" (takes approx 1 minute)"
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
	for VENV in "${VENVS[@]}"
	do
		_install_venv $VENV "echo"
	done
}

# Installs a python executable primed with setuptools, pip & virtualenv.
_install_python()
{
	log "... installing python "$PYTHON_VERSION" (takes approx 3 minutes)"

	# Download source.
	set_working_dir $DIR_PYTHON
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
	log "... installing repo :: $1"

	rm -rf $DIR_REPOS/$1
	git clone -q https://github.com/ES-DOC/$1.git $DIR_REPOS/$1
}

# Installs git repos.
_install_repos()
{
	for REPO in "${REPOS[@]}"
	do
		_install_repo $REPO
	done
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
run_install()
{
	log "INSTALLING STACK"

	_install_dirs
	_install_repos
	_install_python
	_install_venvs
	reset_tmp

	log "INSTALLED STACK"
}

# ###############################################################
# SECTION: UPDATE
# ###############################################################

# Displays information notice upon update.
_update_notice()
{
	log_banner
	log "IMPORTANT NOTICE"
	log "The update process created new config files:" 1
	log "./esdoc/config.json" 2
	log "./esdoc/exec.config" 2
	log "It also created a backup of your old config files:" 1
	log "./esdoc/config.json-backup" 2
	log "./esdoc/exec.config-backup" 2
	log "Please verify your local configuration settings accordingly." 1
	log "IMPORTANT NOTICE ENDS"
}

_update_venv()
{
	log "... updating virtual environment :: $1"

	_uninstall_venv $1
	_install_venv $1
}

# updates virtual environments.
run_update_venvs()
{
	export PATH=$DIR_PYTHON/bin:$PATH

	for VENV in "${VENVS[@]}"
	do
		_update_venv $VENV
	done
}

# Updates a repo.
_update_repo()
{
	log "... updating repo: $1"

	set_working_dir $DIR_REPOS/$1
	git pull -q
	set_working_dir
}

# Updates repos.
run_update_repos()
{
	for REPO in "${REPOS[@]}"
	do
		_update_repo $REPO
	done
}

# Updates config file.
_update_config()
{
	log "... updating configuration"

	cp ./exec.config ./exec.config-backup
	cp ./config.json ./config.json-backup
	cp $DIR_TEMPLATES/template-config.json $DIR/config.json
	cp $DIR_TEMPLATES/template-exec.config $DIR/exec.config
}

# Updates shell.
run_update_shell()
{
	log "... updating shell"

	set_working_dir
	git pull -q
}

# Updates stack.
update()
{
	log "UPDATING STACK"

	run_update_shell
	_update_config
	run_update_repos
	run_update_venvs

	log "UPDATED STACK"

	_update_notice
}

# ###############################################################
# SECTION: UNINSTALL
# ###############################################################

# Uninstalls shell.
_uninstall_shell()
{
	log "... uninstalling shell"

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
	log "... uninstalling repos"

	for REPO in "${REPOS[@]}"
	do
		_uninstall_repo $REPO
	done
}

# Uninstalls python.
_uninstall_python()
{
	log "... uninstalling python"

	rm -rf $DIR_PYTHON
}

# Uninstalls a virtual environment.
_uninstall_venv()
{
	if [ "$2" ]; then
		log "... uninstalling virtual environment :: $1"
	fi

	rm -rf $DIR_VENV/$1
}

# Uninstalls virtual environments.
_uninstall_venvs()
{
	for VENV in "${VENVS[@]}"
	do
		_uninstall_venv $VENV "echo"
	done
}

# Uninstalls stack.
run_uninstall()
{
	log "UNINSTALLING STACK"

	_uninstall_venvs
	_uninstall_python
	_uninstall_repos
	_uninstall_shell

	log "UNINSTALLED STACK"
}

