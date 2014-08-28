#!/bin/bash

# Set root path.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

# Initialise shell.
source $DIR/bash/init.sh

# Invoke action.
$ACTION $ACTION_ARG $ACTION_SUBARG1 $ACTION_SUBARG2

# End.
log_banner
exit 0