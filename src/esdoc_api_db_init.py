#  Module imports.
import sys

import esdoc_api.lib.repo.session as session



# Repo connection string.
_CONNECTION = "postgresql://mqcg:Silence93!@localhost:5432/esdoc_api"

# Input args.
_args = sys.argv[1:]


def _init(connection):
	"""Initialize the target db."""
	# Start session.
	session.start(_CONNECTION)

	# Create repo.
	session.create_repo()

	# Start session.
	session.end()


# Initialize target db.
if not len(_args):
	_init(_CONNECTION)
elif _args[0] == "test":
	_init(_CONNECTION + "_test")
