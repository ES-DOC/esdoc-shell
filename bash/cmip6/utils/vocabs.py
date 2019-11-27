
import pyessv

# Returns set of institutional model configurations.
get_institute_sources = pyessv.WCRP.cmip6.get_institute_sources
get_model_configurations = pyessv.WCRP.cmip6.get_institute_sources

# Returns set of topics associated with a model.
get_model_topics = pyessv.ESDOC.cmip6.getmodel_topics

# Returns set of experiments.
get_experiments = pyessv.WCRP.cmip6.experiment_id

def get_institutes(institution_id=None):
    """Returns set of institutes to be processed.

    """
    return pyessv.WCRP.cmip6.institution_id if institution_id in (None, '', 'all') else \
           [pyessv.WCRP.cmip6.institution_id[institution_id]]