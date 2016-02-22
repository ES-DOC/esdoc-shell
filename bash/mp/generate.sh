#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
	declare ontology=$1
	declare version=$2
	declare language=$3
	activate_venv mp
	python "$ESDOC_DIR_MP/esdoc_mp" -s $ontology -v $version -l $language -o $ESDOC_DIR_TMP
        case "$language" in
          python)
            cp -r "$ESDOC_DIR_TMP/$ontology/v$version" "$ESDOC_DIR_PYESDOC/pyesdoc/ontologies/$ontology"
	    find $ESDOC_DIR_PYESDOC -type f -name "*.pyc" -exec rm -f {} \;
	    find $ESDOC_DIR_PYESDOC -type f -name "*.pye" -exec rm -f {} \;
            ;;
          qxml)
            cp -r "$ESDOC_DIR_TMP/$ontology/v$version" "$ESDOC_DIR_QTN/media/ontologies"
            ;;
          *)
            echo "Invalid language argument. Exiting"
            exit 1;;
        esac
}

# Invoke entry point.
main $1 $2 $3

