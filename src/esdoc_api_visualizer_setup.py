#  Module imports.
from esdoc_api.lib.api import visualizer_setup
import esdoc_api.lib.repo.session as session


# Repo connection string.
_CONNECTION = "postgresql://postgres:Silence107!@localhost:5432/esdoc_api"


# Set of comparators for which to write setup data in json format.
_VISUALIZERS = {
    'CMIP5' : ['v1']
}

# Start session.
session.start(_CONNECTION)


# Write setup json for each supported visualizer.
for project in _VISUALIZERS:
    for type in _VISUALIZERS[project]:
        visualizer_setup.write_visualizer_json(project, type)


# Start session.
session.end()
