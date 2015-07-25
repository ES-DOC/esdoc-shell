#!/bin/bash

# ###############################################################
# SECTION: META-PROGRAMMING FUNCTIONS
# ###############################################################

# Executes meta-programming build process.
run_mp()
{
	declare ontology=$1
	declare version=$2
	declare language=$3

	activate_venv mp
	python "$DIR_MP/esdoc_mp" -s $ontology -v $version -l $language -o $DIR_TMP

	cp -r "$DIR_TMP/$ontology/v$version" "$DIR_PYESDOC/pyesdoc/ontologies/$ontology"

	find $DIR_PYESDOC -type f -name "*.pyc" -exec rm -f {} \;
	find $DIR_PYESDOC -type f -name "*.pye" -exec rm -f {} \;
}

# Executes meta-programming tests.
run_mp_tests()
{
	log "running mp tests ..."

	activate_venv mp

	log "TODO"
}

# Executes meta-programming build against a custom scheme.
run_mp_custom_schema()
{
	log "running mp custom scenario ..."

	log "Step 1.  Running mp utility"
	activate_venv mp
	python "$DIR_MP/esdoc_mp" -s "test" -v "1" -l "python" -o $DIR_TMP

	log "Generated files @ "$DIR_TMP
}
