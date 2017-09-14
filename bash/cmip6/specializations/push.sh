#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Import vocab.
source $ESDOC_HOME/bash/cmip6/specializations/vocab.sh

# Main entry point.
main()
{
	declare comment=$1

	cd $ESDOC_HOME/repos
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		log "CMIP6-SPECS : pushing "$specialization
		cd $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization
		git add .
		git commit -m $comment
		git push -v origin master:master
	done
}

# Invoke entry point.
main $1
