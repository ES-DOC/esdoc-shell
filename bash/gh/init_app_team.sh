#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
    log "SECURITY : initializing GitHub team $1 ..."

	activate_venv
	python $ESDOC_DIR_BASH/gh/init_app_team.py --gh-user=$ESDOC_GITHUB_USER_NAME --oauth-token=$ESDOC_GITHUB_ACCESS_TOKEN --gh-team=$1

    log "SECURITY : $1  GitHub team initialized ..."
}

# Invoke entry point.
main $1
