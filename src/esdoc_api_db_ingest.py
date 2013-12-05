#  Module imports.
import esdoc_api.lib.repo.ingest as ingest
import esdoc_api.lib.repo.session as session



# Repo connection string.
_CONNECTION = "postgresql://postgres:Silence107!@localhost:5432/esdoc_api"


# Start session.
session.start(_CONNECTION)

# Launch ingestion.
ingest.execute()

# Start session.
session.end()