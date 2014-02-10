#!/bin/bash

# ###############################################################
# SECTION: INIT 
# ###############################################################

# Set action.
ACTION=`echo $1 | tr '[:upper:]' '[:lower:]' | tr '-' '_'`

# Set paths:
# ... shell folder
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# ... home folder
DIR_HOME="$( cd "$( dirname "$DIR" )" && pwd )"

# ... web apps folder
DIR_WEBAPPS=$DIR_HOME/webapps

# ... git repos folder
DIR_REPOS=$DIR/repos

# ... path to db backups
DIR_DB_BACKUPS=$DIR"/db/backups"

# Set derived variables:
# ... name of db
DB_NAME=$2"_api_"$3

# ... name of db user
DB_USER=$2"_api_"$3

# ... path to db backup file
DB_FILE=$DIR_DB_BACKUPS"/db"

# ... path to zipped db backup file
DB_FILE_ZIPPED=$DB_FILE".zip"

# # ... api name
# API_NAME=$APP_ENVIRONMENT"_api_"$APP_ID

# # ... api home directory
# API_HOME=$DIR_WEBAPPS/$API_NAME

# API_SOURCE=$API_HOME"/app"
# API_PACKAGE=$API_SOURCE"/esdoc_api"
# API_TEMPLATES=$DIR"/templates"


# List of virtual environments.
TOOLS=(
	'compare'
	'search'
	'view'
	'visualize'
)


# ###############################################################
# SECTION: HELPER FUNCTIONS
# ###############################################################

# Wraps standard echo by adding ES-DOC prefix.
_echo()
{
	tabs=''
	if [ "$1" ]; then
		if [ "$2" ]; then
			for ((i=0; i<$2; i++))
			do
				tabs+='\t'
			done
	    	echo -e 'ES-DOC :: '$tabs$1	
	    else
	    	echo -e "ES-DOC :: "$1	
	    fi
	else
	    echo -e "ES-DOC ::"	
	fi
}

_echo_banner()
{
	echo "---------------------------------------------"
}

# ###############################################################
# SECTION: MAIN
# ###############################################################

# Installs static source code.
_install_source_api()
{
	_echo "TODO: install api source code"
}

# Installs static source code.
_install_source_static()
{
	# ... splash site
	cp -r $DIR_REPOS/esdoc-splash/src/* $DIR_WEBAPPS/$1_$2_splash

	# ... static files
	cp -r $DIR_REPOS/esdoc-static/* $DIR_WEBAPPS/$1_$2_static
	cp -r $DIR_REPOS/esdoc-js-client/demo/media/* $DIR_WEBAPPS/$1_$2_static

	# ... tools
	for TOOL in "${TOOLS[@]}"
	do

		cp -r $DIR_REPOS/esdoc-js-client/demo/* $DIR_WEBAPPS/$1_$2_$TOOL
		mv $DIR_WEBAPPS/$1_$2_$TOOL/$TOOL.html $DIR_WEBAPPS/$1_$2_$TOOL/index.html
		rm -rf $DIR_WEBAPPS/$1_$2_$TOOL/*dev.*
		for _TOOL in "${TOOLS[@]}"
		do
			if [[ $_TOOL != $TOOL ]]; then
				rm -rf $DIR_WEBAPPS/$1_$2_$TOOL/$_TOOL*.*
			fi
		done
	done	
}

# Installs source code.
install_source()
{
	_install_source_api $1 $2
	_install_source_static $1 $2
}

# Restores db from backup.
restore_db()
{
	unzip -q $DB_FILE_ZIPPED -d $DIR_DB_BACKUPS
	pg_restore -U $DB_USER -d $DB_NAME $DB_FILE
	rm $DB_FILE
}

# Restart services.
restart_services()
{
	$DIR_WEBAPPS/$1"_api_"$2/apache2/bin/restart
}

# Stop services.
stop_services()
{
	$DIR_WEBAPPS/$1"_api_"$2/apache2/bin/stop
}


# Invoke action.
$ACTION $2 $3	


# End.
_echo_banner

exit 0