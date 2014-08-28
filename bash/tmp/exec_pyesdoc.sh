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
	    nosetests -v -s $DIR_PYESDOC_TESTS

	# Archive tests.
	elif [ $1 = "a" ]; then
	    log "pyesdoc :: Executing pyesdoc archive tests"
	    nosetests -v -s $DIR_PYESDOC_TESTS/test_archive.py

	# Extension tests.
	elif [ $1 = "e" ]; then
	    log "pyesdoc :: Executing pyesdoc extension tests"
	    nosetests -v -s $DIR_PYESDOC_TESTS/test_extensions.py

	# Factory tests.
	elif [ $1 = "f" ]; then
	    log "pyesdoc :: Executing pyesdoc factory tests"
	    nosetests -v -s $DIR_PYESDOC_TESTS/test_factory.py

	# General tests.
	elif [ $1 = "g" ]; then
	    log "pyesdoc :: Executing pyesdoc general tests"
	    log $DIR_PYESDOC_TESTS/test_general.py
	    nosetests -v -s $DIR_PYESDOC_TESTS/test_general.py

	# Publishing tests.
	elif [ $1 = "p" ]; then
	    log "pyesdoc :: Executing pyesdoc publishing tests"
	    nosetests -v -s $DIR_PYESDOC_TESTS/test_publishing.py

	# Serialization tests.
	elif [ $1 = "s" ]; then
	    log "pyesdoc :: Executing pyesdoc serialization tests"
	    nosetests -v -s $DIR_PYESDOC_TESTS/test_serialization.py

	# Serialization non-ascii tests.
	elif [ $1 = "s-na" ]; then
	    log "pyesdoc :: Executing pyesdoc serialization non-ascii tests"
	    nosetests -v -s $DIR_PYESDOC_TESTS/test_serialization_non_ascii.py

	# Validation tests.
	elif [ $1 = "v" ]; then
	    log "pyesdoc :: Executing pyesdoc validation tests"
	    nosetests -v -s $DIR_PYESDOC_TESTS/test_validation.py
	fi
}

# Executes pyesdoc publishing scenario.
run_pyesdoc_scenario()
{
	log "executing pyesdoc publishing scenario ..."

	activate_venv pyesdoc
	python ./exec_pyesdoc_scenario.py $DIR_TMP
}

# Executes pyesdoc miscellaneous scenario.
run_pyesdoc_misc()
{
	log "executing pyesdoc publishing scenario ..."

	activate_venv pyesdoc
	python $DIR_PYESDOC_MISC/misc.py
}

run_pyesdoc_write_test_files()
{
	log "writing pyesdoc test files ..."

	activate_venv pyesdoc
	python $DIR_PYESDOC_MISC/write_test_files.py
}

run_pyesdoc_write_demo_files()
{
	log "writing pyesdoc demo files ..."

	activate_venv pyesdoc
	python $DIR_PYESDOC_MISC/write_demo_files.py
}

_pyesdoc_help()
{
	log ""
	log "PYESDOC commands :"
	log "pyesdoc-tests" 1
	log "exec pyesdoc automated tests" 2
	log "pyesdoc-scenario" 1
	log "illustrates pyesdoc scenarios" 2
}