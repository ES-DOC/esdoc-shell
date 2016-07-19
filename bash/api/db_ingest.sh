#!/bin/bash

# Activate shell (if necessary).
if [ ! "$ESDOC_HOME" ]; then
    source "$( dirname "$( dirname "$( dirname "${BASH_SOURCE[0]}" )" )" )"/activate
fi

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API-DB: ingesting from pyesdoc archive ..."

    activate_venv api
    python $ESDOC_HOME/bash/api/db_ingest.py

    log "API-DB: ingested from pyesdoc archive"
}

# Invoke entry point.
main
