#!/bin/bash

# ###############################################################
# SECTION: INITIALIZE PATHS
# ###############################################################

declare DIR_BACKUPS=$DIR/ops/backups
declare DIR_BASH=$DIR/bash
declare DIR_DEMOS=$DIR/ops/demos
declare DIR_JOBS=$DIR/ops/jobs
declare DIR_LOGS=$DIR/ops/logs
declare DIR_PYTHON=$DIR/ops/venv/python
declare DIR_REPOS=$DIR/repos
declare DIR_RESOURCES=$DIR/ops/resources
declare DIR_TEMPLATES=$DIR/ops/resources/templates
declare DIR_TMP=$DIR/ops/tmp
declare DIR_VENV=$DIR/ops/venv

declare DIR_API=$DIR_REPOS/esdoc_api
declare DIR_API_SRC=$DIR_REPOS/esdoc-api/src
declare DIR_API_TESTS=$DIR_REPOS/esdoc-api/tests

declare DIR_MP_SRC=$DIR_REPOS/esdoc-mp/src
declare DIR_MP_TESTS=$DIR_REPOS/esdoc-mp/tests

declare DIR_PYESDOC=$DIR_REPOS/esdoc-py-client
declare DIR_PYESDOC_SRC=$DIR_REPOS/esdoc-py-client/src
declare DIR_PYESDOC_TESTS=$DIR_REPOS/esdoc-py-client/tests

declare DIR_QTN_SRC=$DIR_REPOS/esdoc-questionnaire/src

declare DIR_WEB_COMPARATOR=$DIR_REPOS/esdoc-comparator
declare DIR_WEB_PLUGIN=$DIR_REPOS/esdoc-js-client
declare DIR_WEB_STATIC=$DIR_REPOS/esdoc-static
declare DIR_WEB_VIEWER=$DIR_REPOS/esdoc-viewer
