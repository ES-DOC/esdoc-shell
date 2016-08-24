#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

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

# Updates a git repo.
_update_repo()
{
	log "Updating repo: $1"
	set_working_dir $ESDOC_DIR_REPOS/$1
	git pull -q
	remove_files "*.pyc"
	set_working_dir
}

# Main entry point.
main()
{
	log "UPDATING REPOS (LITE)"
	for repo in "${ESDOC_REPOS[@]}"
	do
		if [ $ESDOC_GIT_PROTOCOL != "archive" ]; then
			if [ -d "$ESDOC_DIR_REPOS/$repo" ]; then
				_update_repo $repo
			else
				_install_repo $repo
			fi
		fi
	done
	log "UPDATED REPOS (LITE)"
}

# Invoke entry point.
main
