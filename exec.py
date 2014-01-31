#  Module imports.
import os
import sys

import esdoc_api.lib.api.comparator_setup as comparator_setup
import esdoc_api.lib.api.visualizer_setup as visualizer_setup
import esdoc_api.lib.repo.ingest as ingest
import esdoc_api.lib.repo.session as session
import esdoc_api.lib.repo.utils as repo_utils
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

}


def _start_api_db_session():
	"""Starts an api db session."""
	session.start(cfg.api.db)


def _end_api_db_session():
	"""Ends an api db session."""
	session.end()


def _wrap_api_db_session(task):
	"""Wraps a function with a call to db session start/end."""
	# Start session.
	_start_api_db_session()
	
	# Perform work.
	task()

	# End session.
	_end_api_db_session()


def _db_setup():
	"""Execute db initialization."""
	_wrap_api_db_session(session.create_repo)


def _db_ingest():
	"""Execute db ingestion."""
	_wrap_api_db_session(ingest.execute)


def _api_setup_comparator():
	"""Write api comparator setup data."""
	def _do():
		for project in _COMPARATORS:
		    for type in _COMPARATORS[project]:
		        comparator_setup.write_comparator_json(project, type)

	_wrap_api_db_session(_do)


def _api_setup_visualizer():
	"""Write api visualizer setup data."""
	def _do():
		for project in _VISUALIZERS:
		    for type in _VISUALIZERS[project]:
		        visualizer_setup.write_visualizer_json(project, type)

	_wrap_api_db_session(_do)


def _api_stats():
	"""Write api statistical data."""
	_wrap_api_db_session(repo_utils.write_doc_stats)
	

def _init_config():
	"""Initialize configuration."""
	global cfg

	fp = os.path.dirname(os.path.abspath(__file__))
	fp = os.path.join(fp, "config.json")
	cfg = convert.json_file_to_namedtuple(fp)


# Map of supported actions.
_actions = {
	"db-setup": _db_setup,
	"db-ingest": _db_ingest,
	"api-setup-comparator": _api_setup_comparator,
	"api-setup-visualizer": _api_setup_visualizer,
	"api-stats": _api_stats,
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

