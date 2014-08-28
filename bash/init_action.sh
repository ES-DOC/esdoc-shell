#!/bin/bash

# ###############################################################
# SECTION: INITIALIZE ACTION
# ###############################################################

# Set action.
declare ACTION=`echo $1 | tr '[:upper:]' '[:lower:]' | tr '-' '_'`
if [[ $ACTION != run_* ]]; then
	declare ACTION="run_"$ACTION
fi

# Set action arguments.
declare ACTION_ARG1=$2
declare ACTION_ARG2=$3
declare ACTION_ARG3=$4
