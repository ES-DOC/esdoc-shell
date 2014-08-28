# ###############################################################
# SECTION: JAVASCRIPT PLUGIN FUNCTIONS
# ###############################################################

run_js_plugin_compile()
{
    log "compiling js plugin ..."

	MAKE=$DIR_REPOS/esdoc-js-client/bld/make.sh
	$MAKE $1

    log "compiled js plugin ..."
}

_js_plugin_help()
{
	log ""
	log "Javascript plugin commands :"
	log "js-plugin-compile" 1
	log "compiles es-doc javascript plugin" 2
}