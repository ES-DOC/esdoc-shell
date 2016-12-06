#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	if [ -f $ESDOC_HOME/bash/pyesdoc-mp/validate_report_$1_$2.txt ]; then
		rm $ESDOC_HOME/bash/pyesdoc-mp/validate_report_$1_$2.txt
	fi
	activate_venv pyesdoc
	python $ESDOC_HOME/bash/pyesdoc-mp/validate.py --ontology=$1 --version=$2
}

# Invoke entry point.
main $1 $2
