#  Module imports.
import sys

import esdoc_api.lib.repo.session as session
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.utils as utils



# Repo connection string.
_CONNECTION = "postgresql://postgres:Silence107!@localhost:5432/esdoc_api"

# Start session.
session.start(_CONNECTION)


utils.write_doc_stats()


# Start session.
session.end()
