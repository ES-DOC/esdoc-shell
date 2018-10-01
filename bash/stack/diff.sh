#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Diffs a git repo.
_diff_repo()
{
	echo "DIFFING: "$1
	cd $1
	git diff --shortstat
}

# Diffs git repos.
_diff_repos()
{
	for repo in $(find $1 -maxdepth 1 -mindepth 1 -type d)
	do
		_diff_repo $repo
	done
}

# Main entry point.
main()
{
	log "DIFFING STACK"

	_diff_repo $ESDOC_HOME
	_diff_repos $ESDOC_DIR_REPOS_CORE
	_diff_repos $ESDOC_DIR_REPOS_CMIP6
	_diff_repos $ESDOC_DIR_REPOS_EXT

	log "DIFFING STACK"
}

# Invoke entry point.
main
