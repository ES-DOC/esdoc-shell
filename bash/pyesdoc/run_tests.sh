#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/init.sh

# Main entry point.
main()
{
    log "PYESDOC : running tests ..."
	activate_venv pyesdoc
	# All tests.
	if [ ! "$1" ]; then
	    log "pyesdoc :: Executing all pyesdoc tests"
	    nosetests -v -s $ESDOC_DIR_PYESDOC_TESTS

	# Archive tests.
	elif [ $1 = "a" ]; then
	    log "pyesdoc :: Executing pyesdoc archive tests"
	    nosetests -v -s $ESDOC_DIR_PYESDOC_TESTS/test_archive.py

	# Extension tests.
	elif [ $1 = "e" ]; then
	    log "pyesdoc :: Executing pyesdoc extension tests"
	    nosetests -v -s $ESDOC_DIR_PYESDOC_TESTS/test_extensions.py

	# Factory tests.
	elif [ $1 = "f" ]; then
	    log "pyesdoc :: Executing pyesdoc factory tests"
	    nosetests -v -s $ESDOC_DIR_PYESDOC_TESTS/test_factory.py

	# General tests.
	elif [ $1 = "g" ]; then
	    log "pyesdoc :: Executing pyesdoc general tests"
	    nosetests -v -s $ESDOC_DIR_PYESDOC_TESTS/test_general.py

	# Publishing tests.
	elif [ $1 = "p" ]; then
	    log "pyesdoc :: Executing pyesdoc publishing tests"
	    nosetests -v -s $ESDOC_DIR_PYESDOC_TESTS/test_publishing.py

	# Serialization tests.
	elif [ $1 = "s" ]; then
	    log "pyesdoc :: Executing pyesdoc serialization tests"
	    nosetests -v -s $ESDOC_DIR_PYESDOC_TESTS/test_serialization.py

	# Serialization non-ascii tests.
	elif [ $1 = "s-na" ]; then
	    log "pyesdoc :: Executing pyesdoc serialization non-ascii tests"
	    nosetests -v -s $ESDOC_DIR_PYESDOC_TESTS/test_serialization_non_ascii.py

	# Validation tests.
	elif [ $1 = "v" ]; then
	    log "pyesdoc :: Executing pyesdoc validation tests"
	    nosetests -v -s $ESDOC_DIR_PYESDOC_TESTS/test_validation.py
	fi
}

# Invoke entry point.
main $1
