#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Installs a git repo.
_install_repo()
{
	log "Installing repo: $1"
	rm -rf $ESDOC_DIR_REPOS/$1

	if [ $ESDOC_GIT_PROTOCOL = "ssh" ]; then
		git clone -q git@github.com:ES-DOC/$1.git $DIR_LOCAL_REPOS/$1
	else
		git clone -q https://github.com/ES-DOC/$1.git $ESDOC_DIR_REPOS/$1
	fi
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
}

# Sets up script permissions.
_install_script_permissions()
{
	chmod a+x $ESDOC_HOME/bash/cmip6/*.sh
	chmod a+x $ESDOC_HOME/bash/deployment/*.sh
	chmod a+x $ESDOC_HOME/bash/pyesdoc/*.sh
	chmod a+x $ESDOC_HOME/bash/security/*.sh
	chmod a+x $ESDOC_HOME/bash/stack/*.sh
}

_activate_sub_shells()
{
	source $ESDOC_HOME/repos/esdoc-api/sh/activate
	source $ESDOC_HOME/repos/esdoc-archive/sh/activate
	source $ESDOC_HOME/repos/esdoc-py-client/sh/activate
	source $ESDOC_HOME/repos/esdoc-cdf2cim/sh/activate
	source $ESDOC_HOME/repos/esdoc-cdf2cim-ws/sh/activate
	source $ESDOC_HOME/repos/esdoc-errata-ws/sh/activate
	source $ESDOC_HOME/repos/esdoc-web-plugin/sh/activate
}

# Main entry point.
main()
{
	log "INSTALLING STACK"

	_install_dirs
	_install_script_permissions
	_install_repos
	_activate_sub_shells

	log "INSTALLED STACK"
}

# Invoke entry point.
main
