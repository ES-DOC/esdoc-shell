#!/bin/bash

# Set root path.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

# Initialise shell.
source $DIR/bash/init.sh

# Invoke action.
$ACTION $ACTION_ARG1 $ACTION_ARG2 $ACTION_ARG3

# End.
exit 0