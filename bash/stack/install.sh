#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Installs git repos.
_install_repos()
{
	log "Installing repos"

	mkdir -p $ESDOC_DIR_REPOS_CORE
	mkdir -p $ESDOC_DIR_REPOS_CMIP6
	mkdir -p $ESDOC_DIR_REPOS_INSTITUTIONAL

	for repo in "${ESDOC_REPOS_CORE[@]}"
	do
		log "Installing core repo: $repo"
		rm -rf $ESDOC_DIR_REPOS_CORE/$repo
		git clone -q https://github.com/ES-DOC/$repo.git $ESDOC_DIR_REPOS_CORE/$repo
	done

	for repo in "${ESDOC_REPOS_CMIP6[@]}"
	do
		log "Installing cmip6 repo: $repo"
		rm -rf $ESDOC_DIR_REPOS_CMIP6/$repo
		git clone -q https://github.com/ES-DOC/$repo.git $ESDOC_DIR_REPOS_CMIP6/$repo
	done

	for institution in "${INSTITUTION_ID[@]}"
	do
		log "Installing institutional repo: $institution"
		rm -rf $ESDOC_DIR_REPOS_INSTITUTIONAL/$institution
		git clone -q https://github.com/ES-DOC-INSTITUTIONAL/$institution.git $ESDOC_DIR_REPOS_INSTITUTIONAL/$institution
	done
}

# Main entry point.
main()
{
	log "INSTALLING STACK"

	_install_repos
	activate_sub_shells

	log "INSTALLED STACK"
}

# Invoke entry point.
main
