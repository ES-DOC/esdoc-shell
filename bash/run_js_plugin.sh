#!/bin/bash

# ###############################################################
# SECTION: JAVASCRIPT PLUGIN FUNCTIONS
# ###############################################################

run_js_plugin_compile()
{
    log "compiling js plugin ..."

	source $DIR_BASH/run_js_plugin_build.sh $1

    log "compiled js plugin ..."
}
