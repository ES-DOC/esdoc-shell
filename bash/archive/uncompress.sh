#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	rm -rf $ESDOC_DIR_ARCHIVE/esdoc
	set_working_dir $ESDOC_DIR_ARCHIVE
	cat docs_* | tar xz
	set_working_dir
}

# Invoke entry point.
main