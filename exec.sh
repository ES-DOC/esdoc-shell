#!/bin/bash

# Set root path.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Import associated scripts.
source $DIR/exec_init.sh
source $DIR/exec_api.sh
source $DIR/exec_archive.sh
source $DIR/exec_db.sh
source $DIR/exec_help.sh
source $DIR/exec_install.sh
source $DIR/exec_js_plugin.sh
source $DIR/exec_mp.sh
source $DIR/exec_pyesdoc.sh

# Invoke action.
$ACTION $ACTION_ARG1 $ACTION_ARG2 $ACTION_ARG3

# End.
log_banner
exit 0