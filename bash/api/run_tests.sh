#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "API-TESTS : running ..."

    mkdir -p $ESDOC_DIR_ARCHIVE/esdoc/test-project/unit-test
	activate_venv api
    nosetests -v -s $ESDOC_DIR_API_TESTS

    log "API-TESTS : cleaning up ..."
    source $ESDOC_HOME/bash/archive/delete_documents.sh "test-project"
    source $ESDOC_HOME/bash/api/db_flush.sh "test-project"

    log "API-TESTS : complete ..."
}

# Invoke entry point.
main
