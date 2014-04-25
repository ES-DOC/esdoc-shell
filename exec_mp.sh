# ###############################################################
# SECTION: META-PROGRAMMING FUNCTIONS
# ###############################################################

# Executes meta-programming build process.
run_mp()
{
    log "running mp build ..."

	log "Step 1.  Running mp utility"
	activate_venv mp
	python "$DIR_SRC_MP/esdoc_mp" -s "cim" -v "1" -l "python" -o $DIR_TMP

	log "Step 2.  Copying generated files to pyesdoc"
	cp -r "$DIR_TMP/cim/v1" "$DIR_SRC_PYESDOC/pyesdoc/ontologies/cim"

	log "Step 3.  Copying generated files to api"
	cp -r $DIR_SRC_PYESDOC/pyesdoc $DIR_LIB_API

	log "Step 4.  Cleaning up"
	find $DIR_SRC_PYESDOC -type f -name "*.pyc" -exec rm -f {} \;
	find $DIR_SRC_PYESDOC -type f -name "*.pye" -exec rm -f {} \;
	find $DIR_LIB_API -type f -name "*.pyc" -exec rm -f {} \;
	find $DIR_LIB_API -type f -name "*.pye" -exec rm -f {} \;
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
	python "$DIR_SRC_MP/esdoc_mp" -s "test" -v "1" -l "python" -o $DIR_TMP

	log "Generated files @ "$DIR_TMP
}