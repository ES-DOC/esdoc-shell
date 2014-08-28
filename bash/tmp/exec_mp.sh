# ###############################################################
# SECTION: META-PROGRAMMING FUNCTIONS
# ###############################################################

# Executes meta-programming build process.
run_mp()
{
    log "running mp build ..."

	log "Step 1.  Running mp utility"
	activate_venv mp
	python "$DIR_MP_SRC/esdoc_mp" -s "cim" -v "1" -l "python" -o $DIR_TMP

	log "Step 2.  Copying generated files to pyesdoc"
	cp -r "$DIR_TMP/cim/v1" "$DIR_PYESDOC_SRC/pyesdoc/ontologies/cim"

	log "Step 3.  Cleaning up"
	find $DIR_PYESDOC_SRC -type f -name "*.pyc" -exec rm -f {} \;
	find $DIR_PYESDOC_SRC -type f -name "*.pye" -exec rm -f {} \;
}

# Executes meta-programming tests.
run_mp_tests()
{
	log "running mp tests ..."

	activate_venv mp

	log "TODO"
}

# Executes meta-programming build against a custim scheme.
run_mp_custom_schema()
{
	log "running mp custom scenario ..."

	log "Step 1.  Running mp utility"
	activate_venv mp
	python "$DIR_MP_SRC/esdoc_mp" -s "test" -v "1" -l "python" -o $DIR_TMP

	log "Generated files @ "$DIR_TMP
}

_mp_help()
{
	log ""
	log "MP commands :"
	log "mp" 1
	log "builds pyesdoc from meta-programming framework" 2
	log "mp-tests" 1
	log "executes mp automated tests" 2
	log "mp-custom-schema" 1
	log "runs mp against a custom schema as proof of concept" 2
	log "mp-write-demo-files" 1
	log "writes files used for viewer demos to file system" 2
	log "mp-write-test-files" 1
	log "writes files used for unit tests to file system" 2
}