#  Module imports.
import esdoc_api.lib.api.comparator_setup as comparator_setup
import esdoc_api.lib.repo.session as session


# Repo connection string.
_CONNECTION = "postgresql://postgres:Silence107!@localhost:5432/esdoc_api"


# Set of comparators for which to write setup data in json format.
_COMPARATORS = {
    'CMIP5' : ['c1']
}

# Start session.
session.start(_CONNECTION)


# Write setup json for each supported comparator.
for project in _COMPARATORS:
    for type in _COMPARATORS[project]:
        comparator_setup.write_comparator_json(project, type)


# Start session.
session.end()
