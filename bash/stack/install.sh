#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Installs git repos.
_install_repo()
{
	mkdir -p $1
	cd $1
	log "... "$2" -> "$1
	git clone -q $2
}

# Main entry point.
main()
{
	log "INSTALLING STACK"

	for repo in "${ESDOC_REPOS_CORE[@]}"
	do
		_install_repo $ESDOC_DIR_REPOS_CORE $repo
	done

	for repo in "${ESDOC_REPOS_CMIP6[@]}"
	do
		_install_repo $ESDOC_DIR_REPOS_CMIP6 $repo
	done

	for repo in "${ESDOC_REPOS_EXT[@]}"
	do
		_install_repo $ESDOC_DIR_REPOS_EXT $repo
	done

	activate_sub_shells

	log "INSTALLED STACK"
}

# Invoke entry point.
main
