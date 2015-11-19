#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	$ESDOC_HOME/ops/venv/python/bin/python $ESDOC_HOME/bash/deployment/deploy.py rollout $1 $2 $3 $4 $5
}

# Invoke entry point.
main $1 $2 $3 $4 $5
