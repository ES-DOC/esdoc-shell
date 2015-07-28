#!/bin/bash

# ###############################################################
# SECTION: INITIALIZE PATHS
# ###############################################################

declare DIR_DEFAULT_ARCHIVE=$DIR/archive
declare DIR_BACKUPS=$DIR/ops/backups
declare DIR_BASH=$DIR/bash
declare DIR_CONFIG=$DIR/ops/config
declare DIR_DAEMONS=$DIR/ops/daemons
declare DIR_LOGS=$DIR/ops/logs
declare DIR_PYTHON=$DIR/ops/venv/python
declare DIR_REPOS=$DIR/repos
declare DIR_RESOURCES=$DIR/resources
declare DIR_TMP=$DIR/ops/tmp
declare DIR_VENV=$DIR/ops/venv

declare DIR_API=$DIR_REPOS/esdoc-api
declare DIR_API_TESTS=$DIR_REPOS/esdoc-api/tests

declare DIR_MP=$DIR_REPOS/esdoc-mp
declare DIR_MP_TESTS=$DIR_REPOS/esdoc-mp/tests

declare DIR_PYESDOC=$DIR_REPOS/esdoc-py-client
declare DIR_PYESDOC_TESTS=$DIR_REPOS/esdoc-py-client/tests

declare DIR_QTN_SRC=$DIR_REPOS/esdoc-questionnaire/src

declare DIR_WEB_COMPARATOR=$DIR_REPOS/esdoc-comparator
declare DIR_WEB_PLUGIN=$DIR_REPOS/esdoc-js-client
declare DIR_WEB_STATIC=$DIR_REPOS/esdoc-static
declare DIR_WEB_VIEWER=$DIR_REPOS/esdoc-viewer
