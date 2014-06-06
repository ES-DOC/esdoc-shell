# ###############################################################
# SECTION: JAVASCRIPT PLUGIN FUNCTIONS
# ###############################################################

run_js_plugin_build()
{
    log "building js plugin ..."

	MAKE=$DIR_REPOS/esdoc-js-client/bld/make.sh
	$MAKE $1

    log "built js plugin ..."
}