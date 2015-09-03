#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Upgrades a virtual environment.
_upgrade_venv()
{
	log "Upgrading virtual environment :: $1"
	declare TARGET_VENV=$ESDOC_DIR_VENV/$1
	declare TARGET_VENV_REQUIREMENTS=$ESDOC_DIR_TEMPLATES/venv-requirements-$1.txt
    source $TARGET_VENV/bin/activate
    pip install -q --allow-all-external --upgrade -r $TARGET_VENV_REQUIREMENTS
}


# Main entry point.
main()
{
	log "UPGRADING VIRTUAL ENVIRONMENTS"
	export PATH=$ESDOC_DIR_PYTHON/bin:$PATH
	export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_PYTHON
	for venv in "${ESDOC_VENVS[@]}"
	do
		_upgrade_venv $venv
	done
	log "UPGRADED VIRTUAL ENVIRONMENTS"
}

# Invoke entry point.
main