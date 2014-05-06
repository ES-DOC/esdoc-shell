# ###############################################################
# SECTION: PYESDOC FUNCTIONS
# ###############################################################

# Executes pyesdoc tests.
run_pyesdoc_tests()
{
	log "executing pyesdoc tests ..."

	activate_venv pyesdoc

	# All tests.
	if [ ! "$1" ]; then
	    log "pyesdoc :: Executing all pyesdoc tests"
	    nosetests -v -s $DIR_TESTS_PYESDOC

	# Factory tests.
	elif [ $1 = "f" ]; then
	    log "pyesdoc :: Executing pyesdoc factory tests"
	    nosetests -v -s $DIR_TESTS_PYESDOC/test_factory.py

	# Serialization tests.
	elif [ $1 = "s" ]; then
	    log "pyesdoc :: Executing pyesdoc serialization tests"
	    nosetests -v -s $DIR_TESTS_PYESDOC/test_serialization.py

	# Serialization non-ascii tests.
	elif [ $1 = "s-na" ]; then
	    log "pyesdoc :: Executing pyesdoc serialization non-ascii tests"
	    nosetests -v -s $DIR_TESTS_PYESDOC/test_serialization_non_ascii.py

	# Publishing tests.
	elif [ $1 = "p" ]; then
	    log "pyesdoc :: Executing pyesdoc publishing tests"
	    nosetests -v -s $DIR_TESTS_PYESDOC/test_publishing.py

	# Parsing tests.
	elif [ $1 = "pr" ]; then
	    log "pyesdoc :: Executing pyesdoc parsing tests"
	    nosetests -v -s $DIR_TESTS_PYESDOC/test_parsing.py

	# Validation tests.
	elif [ $1 = "v" ]; then
	    log "pyesdoc :: Executing pyesdoc validation tests"
	    nosetests -v -s $DIR_TESTS_PYESDOC/test_validation.py

	# General tests.
	elif [ $1 = "g" ]; then
	    log "pyesdoc :: Executing pyesdoc general tests"
	    nosetests -v -s $DIR_TESTS_PYESDOC/test_general.py
	fi
}

# Executes pyesdoc publishing scenario.
run_pyesdoc_scenario()
{
	log "executing pyesdoc publishing scenario ..."

	activate_venv pyesdoc
	python ./exec_pyesdoc_scenario.py $DIR_TMP
}

run_pyesdoc_write_test_files()
{
	log "writing pyesdoc test files ..."

	activate_venv pyesdoc
	python $DIR_MISC_PYESDOC/write_test_files.py
}

run_pyesdoc_write_demo_files()
{
	log "writing pyesdoc demo files ..."

	activate_venv pyesdoc
	python $DIR_MISC_PYESDOC/write_demo_files.py
}
