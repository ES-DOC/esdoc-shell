#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Main entry point.
main()
{
    log "GITHUB : cloning institutional repos ..."

    mkdir $ESDOC_HOME/repos/institutional
    cd $ESDOC_HOME/repos/institutional

    for institution_id in "${INSTITUTION_ID[@]}"
    do
      git clone https://github.com/ES-DOC-INSTITUTIONAL/$institution_id.git
    done

    log "GITHUB : institutional repos cloned"
}

# Invoke entry point.
main
