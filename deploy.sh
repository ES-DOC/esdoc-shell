#!/bin/bash

# ###############################################################
# SECTION: INIT
# ###############################################################

# Set action.
declare ACTION=`echo $1 | tr '[:upper:]' '[:lower:]' | tr '-' '_'`

# Set paths.
declare DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
declare DIR_HOME="$( cd "$( dirname "$DIR" )" && pwd )"
declare DIR_REPOS=$DIR"/repos"
declare DIR_RESOURCES=$DIR"/ops/resources/deployment"
declare DIR_TMP=$DIR"/ops/tmp"
declare DIR_WEBAPPS=$DIR_HOME"/webapps"

# Set vars:
declare API_NAME=$2"_"$3"_api"
declare API_HOME=$DIR_WEBAPPS/$API_NAME
declare API_DB_FILE=$DIR_RESOURCES"/api-db"
declare API_DB_FILE_ZIPPED=$API_DB_FILE".zip"
declare API_DB_NAME=$2"_"$3"_api"
declare API_DB_USER=$2"_"$3"_api"


# ###############################################################
# SECTION: HELPER FUNCTIONS
# ###############################################################

# Wraps standard echo by adding ES-DOC prefix.
log()
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
log_banner()
{
	echo "---------------------------------------------"
}

# Resets temporary folder.
reset_tmp()
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
	cp -r $DIR_REPOS/esdoc-py-client/src/* $API_HOME/app

	# ... copy templates to temp folder
	cp -r $DIR_RESOURCES/template-*.* $DIR_TMP
	ls $DIR_TMP

	# ... format templates
	declare -a templates=(
	        $DIR_TMP"/template-config.json"
	        $DIR_TMP"/template-api-httpd.conf"
	        $DIR_TMP"/template-index.py"
	)
	for template in "${templates[@]}"
	do
	        perl -e "s/API_NAME/"$API_NAME"/g;" -pi $(find $template -type f)
	        perl -e "s/API_ENVIRONMENT/"$1"/g;" -pi $(find $template -type f)
	        perl -e "s/API_VERSION/"$2"/g;" -pi $(find $template -type f)
	        perl -e "s/API_DB_USER/"$API_DB_USER"/g;" -pi $(find $template -type f)
	        perl -e "s/API_DB_NAME/"$API_DB_NAME"/g;" -pi $(find $template -type f)
	        perl -e "s/API_DB_PWD/"$3"/g;" -pi $(find $template -type f)
	        perl -e "s/API_PORT/"$4"/g;" -pi $(find $template -type f)
	done

	# ... copy formatted templates
	mv $DIR_TMP"/template-config.json" $API_HOME/app"/.esdoc"
	mv $DIR_TMP"/template-api-httpd.conf" $API_HOME"/apache2/conf/httpd.conf"
	mv $DIR_TMP"/template-index.py" $API_HOME"/htdocs/index.py"

	# ... clear up temp files.
	reset_tmp
}

# Installs static source code.
_install_source_static()
{
	# ... comparator micro-site
	cp -r $DIR_REPOS/esdoc-comparator/src/* $DIR_WEBAPPS/$1_$2_compare
	rm $DIR_WEBAPPS/$1_$2_compare/index-dev.html

	# ... search micro-site
	cp -r $DIR_REPOS/esdoc-search/src/* $DIR_WEBAPPS/$1_$2_search

	# ... splash micro-site
	cp -r $DIR_REPOS/esdoc-splash/src/* $DIR_WEBAPPS/$1_$2_splash

	# ... static files
	cp -r $DIR_REPOS/esdoc-static/* $DIR_WEBAPPS/$1_$2_static
	cp -r $DIR_REPOS/esdoc-js-client/bin/latest/* $DIR_WEBAPPS/$1_$2_static

	# ... viewer micro-site
	cp -r $DIR_REPOS/esdoc-viewer/src/* $DIR_WEBAPPS/$1_$2_view

	# ... viewer demo micro-site
	cp -r $DIR_REPOS/esdoc-static/demos/viewer/* $DIR_WEBAPPS/$1_$2_demo
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
	unzip -q $API_DB_FILE_ZIPPED -d $DIR_RESOURCES
	pg_restore -U $API_DB_USER -d $API_DB_NAME $API_DB_FILE
	rm $API_DB_FILE
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
reset_tmp

# End.
log_banner

exit 0