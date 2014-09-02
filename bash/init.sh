#!/bin/bash

declare -a initializers=(
	'init_action'
	'init_helpers'
	'init_paths'
	'init_vars'
	'run_api'
	'run_api_db'
	'run_archive'
	'run_doc'
	'run_js_plugin'
	'run_help'
	'run_mp'
	'run_pyesdoc'
	'run_stack'
)
for initializer in "${initializers[@]}"
do
	source $DIR/bash/$initializer.sh
done

reset_tmp