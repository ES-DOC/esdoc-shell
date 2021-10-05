#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

_update_repo()
{
	echo "UPDATING: "$1
	cd $1
	git pull
}

# Updates git repos.
_update_repos()
{
	for repo in $(find $1 -maxdepth 1 -mindepth 1 -type d)
	do
		_update_repo $repo
	done
}

# Main entry point.
main()
{
	log "UPDATING STACK"

	_update_repo $ESDOC_HOME
	_update_repos $ESDOC_DIR_REPOS_CORE
	_update_repos $ESDOC_DIR_REPOS_EXT

	log "UPDATED STACK"
}

# Invoke entry point.
main
