#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Installs git repos.
_install_repos()
{
	log "Installing repos"

	mkdir -p $ESDOC_DIR_REPOS
	mkdir -p $ESDOC_DIR_REPOS/core
	for repo in "${ESDOC_REPOS[@]}"
	do
		log "Installing repo: $repo"
		rm -rf ./$repo
		git clone -q https://github.com/ES-DOC/$repo.git
	done

	mkdir -p $ESDOC_DIR_REPOS/cmip6
	for repo in "${ESDOC_REPOS_CMIP6[@]}"
	do
		log "Installing repo: $repo"
		rm -rf $ESDOC_DIR_REPOS/cmip6/$repo
		git clone -q https://github.com/ES-DOC/$repo.git $ESDOC_DIR_REPOS/cmip6/$repo
	done

	mkdir -p $ESDOC_DIR_REPOS/institutional
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
	mkdir -p $ESDOC_DIR_REPOS/cmip6
	mkdir -p $ESDOC_DIR_REPOS/core
	mkdir -p $ESDOC_DIR_REPOS/institutional
}

# Sets up script permissions.
_install_script_permissions()
{
	chmod a+x $ESDOC_HOME/bash/cmip6/experiments/*.sh
	chmod a+x $ESDOC_HOME/bash/cmip6/models/*.sh
	chmod a+x $ESDOC_HOME/bash/cmip6/specializations/*.sh
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
	# _activate_sub_shells

	log "INSTALLED STACK"
}

# Invoke entry point.
main
