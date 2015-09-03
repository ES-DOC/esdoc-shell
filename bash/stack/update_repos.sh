#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Installs a git repo.
_install_repo()
{
	log "Installing repo: $1"
	rm -rf $ESDOC_DIR_REPOS/$1
	git clone -q https://github.com/ES-DOC/$1.git $ESDOC_DIR_REPOS/$1
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
	log "UPDATING REPOS"
	for repo in "${ESDOC_REPOS[@]}"
	do
		if [ -d "$ESDOC_DIR_REPOS/$repo" ]; then
			_update_repo $repo
		else
			_install_repo $repo
		fi
	done
	log "UPDATED REPOS"
}

# Invoke entry point.
main
