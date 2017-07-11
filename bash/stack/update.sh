#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
_update_shell()
{
	log "UPDATING SHELL"
	set_working_dir
	git pull -q
	remove_files "*.pyc"
	log "UPDATED SHELL"
}

# Updates a git repo.
_update_repo()
{
	declare target=$1
	declare dir_repo=$2"/$1"
	declare gh_repo=$3"/$1.git"
	echo $target $dir_repo $gh_repo
	# if [ -d "$dir_repo" ]; then
	# 	log "Updating core repo: $target"
	# 	set_working_dir $dir_repo
	# 	git pull -q
	# 	remove_files "*.pyc"
	# 	set_working_dir
	# else
	# 	log "Installing core repo: $target"
	# 	rm -rf $dir_repo
	# 	git clone -q $gh_repo $dir_repo
	# fi
}

# Updates git repos.
_update_repos()
{
	log "UPDATING REPOS"

	mkdir -p $ESDOC_DIR_REPOS
	mkdir -p $ESDOC_DIR_REPOS_CORE
	for repo in "${ESDOC_REPOS[@]}"
	do
		_update_repo $repo $ESDOC_DIR_REPOS "https://github.com/ES-DOC"
	done

	mkdir -p $ESDOC_DIR_REPOS_CMIP6
	for repo in "${ESDOC_REPOS_CMIP6[@]}"
	do
		_update_repo $repo $ESDOC_DIR_REPOS_CMIP6 "https://github.com/ES-DOC"
	done

	mkdir -p $ESDOC_DIR_REPOS/institutional
	for institution in "${INSTITUTION_ID[@]}"
	do
		_update_repo $institution $ESDOC_DIR_REPOS_INSTITUTIONAL "https://github.com/ES-DOC-INSTITUTIONAL"
	done

	log "UPDATED REPOS"
}

# Main entry point.
main()
{
	log "UPDATING STACK"

	_update_shell
	_update_repos

	log "UPDATED STACK"
}

# Invoke entry point.
main
