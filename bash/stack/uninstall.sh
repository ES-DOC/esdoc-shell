#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Uninstalls shell.
_uninstall_shell()
{
	log "Uninstalling shell"
	rm -rf $ESDOC_HOME
}

# Uninstalls git repos.
_uninstall_repos()
{
	log "Uninstalling repos"
	rm -rf $ESDOC_DIR_REPOS
}

# Uninstalls python.
_uninstall_python()
{
	log "Uninstalling python"
	rm -rf $ESDOC_DIR_PYTHON
}

# Uninstalls a virtual environment.
_uninstall_venv()
{
	if [ "$2" ]; then
		log "Uninstalling virtual environment :: $1"
	fi
	rm -rf $ESDOC_DIR_VENV/$1
}

# Uninstalls virtual environments.
_uninstall_venvs()
{
	for venv in "${ESDOC_VENVS[@]}"
	do
		_uninstall_venv $venv "echo"
	done
}

# Main entry point.
main()
{
	log "UNINSTALLING STACK"

	_uninstall_venvs
	_uninstall_python
	_uninstall_repos
	_uninstall_shell

	log "UNINSTALLED STACK"
}

# Invoke entry point.
main
