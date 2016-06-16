#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	export PYTHONPATH=$PYTHONPATH:$ESDOC_DIR_NB

	declare dest=$ESDOC_DIR_REPOS/esdoc-cim/v2/schema
	rm $dest/*.py
	python $ESDOC_HOME/bash/nb/rewrite_cim2_schema.py --dest=$dest
}

# Invoke entry point.
main
