#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_NB

	python $ESDOC_HOME/bash/nb/rewrite_cmip6_specializations.py --dest=$ESDOC_DIR_REPOS/esdoc-mp/esdoc_mp/specializations/cmip6
}

# Invoke entry point.
main
