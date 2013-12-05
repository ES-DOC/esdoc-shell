#  Module imports.
import sys

import esdoc_api.lib.repo.session as session
import esdoc_api.lib.repo.dao as dao



# Repo connection string.
_CONNECTION = "postgresql://postgres:Silence107!@localhost:5432/esdoc_api"

# Start session.
session.start(_CONNECTION)


print dao.get_project_institute_type_counts()


# Start session.
session.end()
