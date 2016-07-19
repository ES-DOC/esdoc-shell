#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	log "ARCHIVE: deleting archived documents ..."

	if [ "$2" ]; then
		declare target=$ESDOC_DIR_ARCHIVE/esdoc/$1/$2
		rm -rf $target/*.*
	else
		declare target=$ESDOC_DIR_ARCHIVE/esdoc/$1
		rm -rf $target
	fi

	log "ARCHIVE: deleted archived documents from "$target
}

# Invoke entry point.
main $1 $2