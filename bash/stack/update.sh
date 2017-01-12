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

# Updates git repos.
_update_repos()
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

# Main entry point.
main()
{
	log "UPDATING STACK"

	_update_shell
	_update_repos

	source $ESDOC_HOME/bash/stack/upgrade_venvs.sh

	log "UPDATED STACK"
}

# Invoke entry point.
main
