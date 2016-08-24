#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Upgrades a virtual environment.
_upgrade_venv()
{
	log "Upgrading virtual environment :: $1"
	declare TARGET_VENV=$ESDOC_DIR_VENV/$1
    source $TARGET_VENV/bin/activate
    pip install -q --force-reinstall --no-cache-dir --upgrade -r $ESDOC_DIR_RESOURCES/venv-requirements-$1.txt
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