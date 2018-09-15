#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Import vocab.
source $ESDOC_DIR_BASH/cmip6/specializations/vocab.sh

# Main entry point.
main()
{
	declare comment=$1

	# Push specializations.
	cd $ESDOC_HOME/repos
	for specialization in "${CMIP6_SPECIALIZATIONS[@]}"
	do
		log "CMIP6-SPECS : pushing "$specialization
		cd $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization
		git add .
		git commit -m $comment
		git push -v origin master:master
	done

	# Push viewer.
	cd $ESDOC_HOME/repos/esdoc-web-view-specialization
	git add .
	git commit -m $comment
	git push -v origin master:master
}

# Invoke entry point.
main $1
