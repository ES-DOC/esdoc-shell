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

# Set path: tmp.
DIR_TMP=$DIR"/tmp"

# ... web apps folder
DIR_WEBAPPS=$DIR_HOME"/webapps"

# ... templates
DIR_TEMPLATES=$DIR"/templates"

# ... git repos folder
DIR_REPOS=$DIR"/repos"

# ... path to db backups
DIR_DB_BACKUPS=$DIR"/db/backups"

# Set derived variables:
# ... name of db
DB_NAME=$2"_"$3"_api"

# ... name of db user
DB_USER=$2"_"$3"_api"

# ... path to db backup file
DB_FILE=$DIR_DB_BACKUPS"/db"

# ... path to zipped db backup file
DB_FILE_ZIPPED=$DB_FILE".zip"

# ... api name
API_NAME=$2"_"$3"_api"

# ... path to api home
API_HOME=$DIR_WEBAPPS/$API_NAME

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

# Outputs a separator.
_echo_banner()
{
	echo "---------------------------------------------"
}

# Resets temporary folder.
_reset_tmp()
{
	rm -rf $DIR_TMP/*
	mkdir -p $DIR_TMP
}

# ###############################################################
# SECTION: MAIN
# ###############################################################


# Installs static source code.
_install_source_api()
{
	# ... create api source code folder
	mkdir -p $API_HOME/app

	# ... copy source code
	cp -r $DIR_REPOS/esdoc-api/src/* $API_HOME/app

	# ... delete obsolete code
	targets=(
	        $API_HOME"/app/esdoc_api/config/ini_files"
	        $API_HOME"/app/esdoc_api/app.wsgi"
	        $API_HOME"/app/esdoc_api/webrun.py"
	)
	for target in "${targets[@]}"
	do
	        rm -rf $target
	done

	# ... copy templates to temp folder
	cp -r $DIR_TEMPLATES $DIR_TMP

	# ... format templates
	templates=(
	        $DIR_TMP"/templates/template-api-config.ini"
	        $DIR_TMP"/templates/template-api-httpd.conf"
	        $DIR_TMP"/templates/template-api-wsgi.py"
	)
	for template in "${templates[@]}"
	do
	        perl -e "s/API_NAME/"$API_NAME"/g;" -pi $(find $template -type f)
	        perl -e "s/API_ENVIRONMENT/"$1"/g;" -pi $(find $template -type f)
	        perl -e "s/API_VERSION/"$2"/g;" -pi $(find $template -type f)
	        perl -e "s/DB_USER/"$DB_USER"/g;" -pi $(find $template -type f)
	        perl -e "s/DB_NAME/"$DB_NAME"/g;" -pi $(find $template -type f)
	        perl -e "s/DB_PWD/"$3"/g;" -pi $(find $template -type f)
	        perl -e "s/API_PORT/"$4"/g;" -pi $(find $template -type f)
	done

	# ... copy formatted templates
	mv $DIR_TMP"/templates/template-api-config.ini" $API_HOME"/app/config.ini"
	mv $DIR_TMP"/templates/template-api-httpd.conf" $API_HOME"/apache2/conf/httpd.conf"
	mv $DIR_TMP"/templates/template-api-wsgi.py" $API_HOME"/htdocs/wsgi.py"

	# ... clear up temp files.
	_reset_tmp
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
	_install_source_api $1 $2 $3 $4
	_install_source_static $1 $2
}

# Restores db from backup.
restore_db()
{
	unzip -q $DB_FILE_ZIPPED -d $DIR_DB_BACKUPS
	pg_restore -U $DB_USER -d $DB_NAME $DB_FILE
	rm $DB_FILE
}

# Restart api.
restart_api()
{
	$DIR_WEBAPPS/$API_NAME/apache2/bin/restart
}

# Stop api.
stop_api()
{
	$DIR_WEBAPPS/$API_NAME/apache2/bin/stop
}


# Invoke action.
$ACTION $2 $3 $4 $5	

# Reset temporary folder.
_reset_tmp

# End.
_echo_banner

exit 0