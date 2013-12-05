#  Module imports.
import esdoc_api.lib.repo.session as session
import esdoc_api.lib.repo.ingest as ingest


# Repo connection string.
_CONNECTION = "postgresql://postgres:Silence107!@localhost:5432/esdoc_api"


# Endpoint = CMIP5 Questionnaire
_EP_01 = 'http://q.cmip5.ceda.ac.uk/feeds/cmip5/all'

# Simulation : ERR = null value in column "Project_ID" violates not-null constraint.
_EP_01_URL_01 = ' http://q.cmip5.ceda.ac.uk/cmip5/simulation/d2113c12-ccff-11e1-ae50-00163e9152a5/1/'

# Simulation (with ensemble): ERR = null value in column "Project_ID" violates not-null constraint.
_EP_01_URL_02 = 'http://q.cmip5.ceda.ac.uk/cmip5/simulation/f134bbba-40f9-11e1-a594-00163e9152a5/1'

# Experiment with document version as a document attribute rather than a documentVersion element.
_EP_01_URL_03 = "http://q.cmip5.ceda.ac.uk/cmip5/experiment/76f85a8a-4830-11e1-8ba0-00163e9152a5/2"

# Model component with facets.
_EP_01_URL_04 = " http://q.cmip5.ceda.ac.uk/cmip5/component/03c6cbaa-fd27-11df-a88e-00163e9152a5/5"

# Old experiment document.
_EP_01_URL_05 = "http://q.cmip5.ceda.ac.uk/cmip5/experiment/581acb8e-4830-11e1-9409-00163e9152a5/1"

# New experiment document.
_EP_01_URL_06 = "http://q.cmip5.ceda.ac.uk/cmip5/experiment/2960be30-8876-11e1-b0c4-0800200c9a66/2"

# GFDL simulation document with invalid DRS tag.
_EP_01_URL_07 = "http://q.cmip5.ceda.ac.uk/cmip5/simulation/7800a084-6169-11e1-bd49-00163e9152a5/2/"


# Endpoint = CMIP5 QC.
_EP_02 = 'http://cera-www.dkrz.de/WDCC/CMIP5/feed'
_EP_02_URL_01 = "http://cera-www.dkrz.de/WDCC/CMIP5/downloadAtomXml?id=26494"


# Endpoint = QED-2013.
_EP_03 = 'http://earthsystemcog.org/metadata/feed/qed-2013/'
_EP_03_FILE_01 = "/Users/markmorgan/Development/sourcetree/esdoc/esdoc-py-client/tests/pyesdoc_test/ontologies/cim/v1_8_1/files/software.statisticalModelComponent.xml"


# Start session.
session.start(_CONNECTION)

# Launch ingestion.
#ingest.ingest_url(_EP_01, _EP_01_URL_02)
ingest.ingest_file(_EP_03, _EP_03_FILE_01)

# Start session.
session.end()
