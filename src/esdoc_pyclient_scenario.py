# Constants.
_INSTITUTE = 'IPSL'
_PROJECT = 'CMIP5'
_OUTPUT_DIR = '/Users/markmorgan/Development/tmp'


# **********************************************************************
# STEP 0 : Importing modules.
# **********************************************************************
import pyesdoc
import pyesdoc.ontologies.cim as cim


# **********************************************************************
# STEP 1 : Creating "documents", i.e. plain old python objects (POPO's).
# **********************************************************************

# ... create model
model = pyesdoc.create(cim.v1.ModelComponent, _PROJECT, _INSTITUTE)
model.short_name = "IPSL-CDX-LR"
print "CREATED DOC :: ID = {0} :: VERSION = {1}".format(model.doc_info.id, 
														model.doc_info.version)

# ... create responsible party.
rp = pyesdoc.create(cim.v1.ResponsibleParty, _PROJECT, _INSTITUTE)
rp.individual_name = "Mark A. Greenslade"
rp.organisation_name = "IPSL"
rp.contact_info.email = "momipsl@ipsl.jussieu.fr"
model.responsible_parties.append(rp)

# ... create citation.
citation = pyesdoc.create(cim.v1.Citation, _PROJECT, _INSTITUTE)
citation.location = "http://dx.doi.org/10.1007/s00382-006-0158-0"
citation.title = "A generated citation."
model.citations.append(citation)

# ... create component
component = pyesdoc.create(cim.v1.ModelComponent, _PROJECT, _INSTITUTE)
component.type = "Atmosphere"
component.short_name = "Atmosphere"
component.long_name = "Atmosphere"
model.sub_components.append(component)

# ... create component property
property = pyesdoc.create(cim.v1.ComponentProperty, _PROJECT, _INSTITUTE)
property.short_name = "Basic Approximations"
property.values = ["hydrostatic | primitive equations"]
component.properties.append(property)

# ... create sub-component
component1 = pyesdoc.create(cim.v1.ModelComponent, _PROJECT, _INSTITUTE)
component1.type = "Atmosphere.ConvectionCloudTurbulence"
component1.short_name = "Convection Cloud Turbulence"
component1.long_name = "Convection Cloud Turbulence"
model.sub_components.append(component1)

# ... create sub-component property
property1 = pyesdoc.create(cim.v1.ComponentProperty, _PROJECT, _INSTITUTE)
property1.short_name = "Deep Convection"
component1.properties.append(property1)

# ... create sub-component sub-property
property11 = pyesdoc.create(cim.v1.ComponentProperty, _PROJECT, _INSTITUTE)
property11.short_name = "Processes"
property11.values = ["detrainment | entrainment | penetrative convection | updrafts and downdrafts | vertical momentum transport"]
property1.sub_properties.append(property11)

# ...etc

# ... create simulation
simulation = pyesdoc.create(cim.v1.SimulationRun, _PROJECT, _INSTITUTE)
simulation.short_name = "IPSL-CDX-LR.piControl"

# ... associate model & simulation.
pyesdoc.associate(simulation, 'model_reference', model)

# ...etc


# **********************************************************************
# Step 2 : Serialization.
# **********************************************************************

# ... encode as json
model_as_json = pyesdoc.encode(model, pyesdoc.ESDOC_ENCODING_JSON)
simulation_as_json = pyesdoc.encode(simulation, pyesdoc.ESDOC_ENCODING_JSON)

# ... encode asxml
model_as_XML = pyesdoc.encode(model, pyesdoc.ESDOC_ENCODING_XML)
simulation_as_XML = pyesdoc.encode(simulation, pyesdoc.ESDOC_ENCODING_XML)

# ... decode from json
model = pyesdoc.decode(model_as_json, pyesdoc.ESDOC_ENCODING_JSON)
simulation = pyesdoc.decode(simulation_as_json, pyesdoc.ESDOC_ENCODING_JSON)


# **********************************************************************
# Step 3 : I/O
# **********************************************************************

# ... set output path.
pyesdoc.set_output_directory(_OUTPUT_DIR)

# ... write to file system.
model_filepath = pyesdoc.write(model)
simulation_filepath = pyesdoc.write(simulation)

# ... Read from file system.
model = pyesdoc.read(model_filepath)
simulation = pyesdoc.read(simulation_filepath)


# **********************************************************************
# STEP 4 : Publishing
# **********************************************************************

# ... publish
pyesdoc.publish(model)
pyesdoc.publish(simulation)

print "PUBLISHED DOC :: ID = {0} :: VERSION = {1}".format(
	model.doc_info.id, model.doc_info.version)

# ... retrieve
model = pyesdoc.retrieve(model.doc_info.id)
model = pyesdoc.retrieve(model.doc_info.id, model.doc_info.version)

# ... republish
model_version = model.doc_info.version
model.short_name = "IPSL-CDX-MR"
pyesdoc.publish(model)
assert model_version + 1 == model.doc_info.version

print "REPUBLISHED DOC :: ID = {0} :: VERSION = {1}".format(
	model.doc_info.id, model.doc_info.version)

# ... unpublish
pyesdoc.unpublish(model.doc_info.id)
pyesdoc.unpublish(simulation.doc_info.id)
