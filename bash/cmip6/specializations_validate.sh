#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	declare specialization=$1
	python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/validate
}

# Invoke entry point.
main $1
