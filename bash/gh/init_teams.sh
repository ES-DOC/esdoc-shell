#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
    log "SECURITY : initializing GitHub team $1 ..."

	activate_venv
	python $ESDOC_HOME/bash/security/init_gh_team.py --gh-user=$ESDOC_GITHUB_USER_NAME --oauth-token=$ESDOC_GITHUB_ACCESS_TOKEN --gh-team=$1

    log "SECURITY : $1  GitHub team initialized ..."
}

# Invoke entry point.
main $1
