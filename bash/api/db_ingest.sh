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
    python $ESDOC_DIR_API/jobs/run_db_ingest.py
    deactivate

    log "API-DB: ingested from pyesdoc archive"
}

# Invoke entry point.
main
