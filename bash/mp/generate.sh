#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	declare ontology=$1
	declare version=$2
	declare language=$3

	if [ $language = "python" ]; then
		declare data=$ESDOC_DIR_TMP/$ontology/v$version
	elif [ $language = "qxml" ]; then
		declare data=$ESDOC_DIR_TMP/$ontology/v$version/$ontology"_"$version.xml
	fi

	activate_venv mp
	python "$ESDOC_DIR_MP/esdoc_mp" -s $ontology -v $version -l $language -o $ESDOC_DIR_TMP

	log_banner
	if [ $language = "python" ]; then
		declare dest=$ESDOC_DIR_PYESDOC/pyesdoc/ontologies/$ontology
		cp -r $data $dest
		log "generated artefacts copied to @ "$dest
	elif [ $language = "qxml" ]; then
		declare dest=$ESDOC_DIR_CIM/v$version/questionnaire/$ontology-v$version-q-config.xml
		cp -r $data $dest
		log "generated artefacts copied to @ "$dest
	fi
	log_banner

	find $ESDOC_DIR_PYESDOC -type f -name "*.pyc" -exec rm -f {} \;
	find $ESDOC_DIR_PYESDOC -type f -name "*.pye" -exec rm -f {} \;
	reset_tmp
}

# Invoke entry point.
main $1 $2 $3
