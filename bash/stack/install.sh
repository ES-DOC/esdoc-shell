#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Installs git repos.
_install_repos()
{
	log "Installing repos"

	mkdir -p $ESDOC_DIR_REPOS
	mkdir -p $ESDOC_DIR_REPOS_CORE
	for repo in "${ESDOC_REPOS[@]}"
	do
		log "Installing core repo: $repo"
		rm -rf ./$repo
		git clone -q https://github.com/ES-DOC/$repo.git $ESDOC_DIR_REPOS/$repo
	done

	mkdir -p $ESDOC_DIR_REPOS_CMIP6
	for repo in "${ESDOC_REPOS_CMIP6[@]}"
	do
		log "Installing cmip6 repo: $repo"
		rm -rf $ESDOC_DIR_REPOS_CMIP6/$repo
		git clone -q https://github.com/ES-DOC/$repo.git $ESDOC_DIR_REPOS_CMIP6/$repo
	done

	mkdir -p $ESDOC_DIR_REPOS/institutional
	for institution in "${INSTITUTION_ID[@]}"
	do
		log "Installing institutional repo: $institution"
		rm -rf $ESDOC_DIR_REPOS_INSTITUTIONAL/$institution
		git clone -q https://github.com/ES-DOC/$institution.git $ESDOC_DIR_REPOS_INSTITUTIONAL/$institution
	done
}

# Sets up operational directories.
_install_ops_dirs()
{
	for ops_dir in "${ESDOC_OPS_DIRS[@]}"
	do
		mkdir -p $ops_dir
	done
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

# Main entry point.
main()
{
	log "INSTALLING STACK"

	_install_ops_dirs
	_install_script_permissions
	_install_repos
	activate_sub_shells

	log "INSTALLED STACK"
}

# Invoke entry point.
main
