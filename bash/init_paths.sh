#!/bin/bash

# ###############################################################
# SECTION: INITIALIZE PATHS
# ###############################################################

declare DIR_BACKUPS=$DIR/ops/backups
declare DIR_BASH=$DIR/bash
declare DIR_DB_BACKUPS=$DIR/ops/backups/db
declare DIR_PYTHON=$DIR/ops/venv/python
declare DIR_REPOS=$DIR/repos
declare DIR_RESOURCES=$DIR/ops/resources
declare DIR_SCRIPTS=$DIR/ops/scripts
declare DIR_TEMPLATES=$DIR/ops/resources/templates
declare DIR_TMP=$DIR/ops/tmp
declare DIR_VENV=$DIR/ops/venv

declare DIR_API=$DIR_REPOS/esdoc_api
declare DIR_API_SRC=$DIR_REPOS/esdoc-api/src
declare DIR_API_TESTS=$DIR_REPOS/esdoc-api/tests

declare DIR_MP_SRC=$DIR_REPOS/esdoc-mp/src
declare DIR_MP_TESTS=$DIR_REPOS/esdoc-mp/tests

declare DIR_PYESDOC_SRC=$DIR_REPOS/esdoc-py-client/src
declare DIR_PYESDOC_TESTS=$DIR_REPOS/esdoc-py-client/tests
declare DIR_PYESDOC_TESTS1=$DIR_REPOS/esdoc-py-client
declare DIR_PYESDOC_MISC=$DIR_REPOS/esdoc-py-client/misc

declare DIR_QTN_SRC=$DIR_REPOS/esdoc-questionnaire/src
