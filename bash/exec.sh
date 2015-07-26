#!/bin/bash

# Set root path.
declare DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ..
declare DIR="$( pwd )"

echo $DIR

# Initialise shell.
source $DIR/bash/init.sh

# Invoke action.
$ACTION $ACTION_ARG1 $ACTION_ARG2 $ACTION_ARG3

# End.
exit 0