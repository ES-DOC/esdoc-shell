#  Module imports.
import os
import sys

import esdoc_api.lib.api.comparator_setup as comparator_setup
import esdoc_api.lib.api.visualizer_setup as visualizer_setup
import esdoc_api.lib.repo.ingest as ingest
import esdoc_api.lib.repo.session as session
import esdoc_api.models as models

from utils import convert


# Script configuration.
cfg = None

# Set of comparators for which to write setup data in json format.
_COMPARATORS = {
    'CMIP5' : ['c1']
}

# Set of visualizers for which to write setup data in json format.
_VISUALIZERS = {
    'CMIP5' : ['v1']
}


def _start_api_db_session():
	"""Starts an api db session."""
	session.start(cfg.api.db)


def _end_api_db_session():
	"""Ends an api db session."""
	session.end()


def _api_db_init():
	"""Execute db initialization."""
	# Start session.
	_start_api_db_session()
	
	# Create repo.
	session.create_repo()

	# End session.
	_end_api_db_session()


def _api_db_ingest():
	"""Execute db ingestion."""
	# Start session.
	_start_api_db_session()
	
	# Launch ingestion.
	ingest.execute()

	# End session.
	_end_api_db_session()


def _api_setup_comparators():
	"""Write api comparator setup data."""
	# Start session.
	_start_api_db_session()
	
	for project in _COMPARATORS:
	    for type in _COMPARATORS[project]:
	        comparator_setup.write_comparator_json(project, type)

	# End session.
	_end_api_db_session()


def _api_setup_visualizers():
	"""Write api visualizer setup data."""
	# Start session.
	_start_api_db_session()
	
	for project in _VISUALIZERS:
	    for type in _VISUALIZERS[project]:
	        visualizer_setup.write_visualizer_json(project, type)

	# End session.
	_end_api_db_session()


def _init_config():
	"""Initialize configuration."""
	global cfg

	fp = os.path.dirname(os.path.abspath(__file__))
	fp = os.path.join(fp, "config.json")
	cfg = convert.json_file_to_namedtuple(fp)


# Map of supported actions.
_actions = {
	"api-db-init": _api_db_init,
	"api-db-ingest": _api_db_ingest,
	"api-setup-comparators": _api_setup_comparators,
	"api-setup-visualizers": _api_setup_visualizers
}

def main():
	"""Main entry point."""
	# Validate action.
	if sys.argv[1] not in _actions:
		raise NotImplementedError(sys.argv[1])

	# Initialize configuration.
	_init_config()

	# Invoke action.
	_actions[sys.argv[1]]()



if __name__ == '__main__':
    main()
