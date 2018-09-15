#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Updates a git repo.
_update_repo()
{
	declare target=$1
	declare dir_repo=$2"/$1"
	declare gh_repo=$3"/$1.git"
	declare repo_type=$4
	if [ -d "$dir_repo" ]; then
		log "Updating $repo_type repo: $target"
		set_working_dir $dir_repo
		git pull -q
		remove_files "*.pyc"
		set_working_dir
	else
		log "Installing $repo_type repo: $target"
		rm -rf $dir_repo
		git clone -q $gh_repo $dir_repo
	fi
}

# Main entry point.
main()
{
	log "UPDATING INSTITUTIONAL REPOS"

	mkdir -p $ESDOC_DIR_REPOS/institutional
	for institution in "${INSTITUTION_ID[@]}"
	do
		_update_repo $institution $ESDOC_DIR_REPOS_INSTITUTIONAL "https://github.com/ES-DOC-INSTITUTIONAL" "institutional"
	done

	log "UPDATED INSTITUTIONAL REPOS"
}

# Invoke entry point.
main
