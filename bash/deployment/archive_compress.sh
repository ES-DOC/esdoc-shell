#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	set_working_dir $ESDOC_DIR_ARCHIVE
	rm -rf docs_*
	tar cz esdoc | split -b 10m - docs_
	set_working_dir
}

# Invoke entry point.
main