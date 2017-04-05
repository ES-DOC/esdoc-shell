#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	if [ -f $ESDOC_HOME/bash/pyesdoc/mp_validate_report_$1_$2.txt ]; then
		rm $ESDOC_HOME/bash/pyesdoc/mp_validate_report_$1_$2.txt
	fi
	activate_venv
	python $ESDOC_HOME/bash/pyesdoc/mp_validate.py --ontology=$1 --version=$2
}

# Invoke entry point.
main $1 $2
