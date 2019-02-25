# -*- coding: utf-8 -*-

"""
.. module:: model_topic.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Model topic notebook data wrapper.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections
import json
import os

from pyesdoc.mp.specializations.utils_cache import get_topic_specialization
from pyesdoc.mp.specializations.utils_cache import get_property_specialization



# Null property value.
_NULL_PROPERTY = lambda: {'values': []}


class ModelTopicOutput(object):
    """Model topic data wrapper.

    """
    def __init__(self, mip_era, institute, source_id, topic, path=None):
        """Instance initialiser.

        """
        self.content = dict()
        self.institute = unicode(institute).strip().lower()
        self.mip_era = unicode(mip_era).strip().lower()
        self.seeding_source = None
        self.source_id = unicode(source_id).strip().lower()
        self.specialization = get_topic_specialization(mip_era, topic)
        self.topic = unicode(topic).strip().lower()
        self._prop = None
        self._prop_specialization = None
        self._init_state(path)


    def _init_state(self, path):
        """Initialises state from file system.

        """
        # Initialise directory path.
        if path is None:
            path = os.path.join(os.path.expanduser('~'), '.esdoc/notebook-output')
            path = os.path.join(path, self.mip_era)
            path = os.path.join(path, 'models')
            path = os.path.join(path, self.source_id)
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join(path, '{}.json'.format(self.topic))

        # Initialise state from previously saved output file.
        self.fpath = path
        if os.path.isfile(self.fpath):
            with open(self.fpath, 'r') as fstream:
                self._from_dict(json.loads(fstream.read()))


    @classmethod
    def create(cls, mip_era, institution_id, source_id, topic_id):
        """Get notebook output wrapper instance.

        """
        # Set path to notebook output file.
        path = os.path.join(os.getenv('JH_ARCHIVE_HOME'), 'data')
        path = os.path.join(path, institution_id)
        path = os.path.join(path, mip_era)
        path = os.path.join(path, 'models')
        path = os.path.join(path, source_id)
        path = os.path.join(path, topic_id)
        path += '.json'

        # Return notebook output wrapper.
        return cls(mip_era, institution_id, source_id, topic_id, path=path)


    def save(self):
        """Persists state to file system.

        """
        with open(self.fpath, 'w') as fstream:
            fstream.write(json.dumps(self._to_dict(), indent=4))


    def _from_dict(self, obj):
        """Initialises internal state from a dictionary.

        """
        self.mip_era = obj['mipEra']
        self.institute = obj['institute']
        self.seeding_source = obj.get('seedingSource')
        self.source_id = obj['sourceID']
        self.topic = obj['topic']
        self.content = obj['content']


    def _to_dict(self):
        """Returns a dictionary representation of internal state.

        """
        obj = collections.OrderedDict()
        obj['mipEra'] = self.mip_era
        obj['institute'] = self.institute
        obj['seedingSource'] = self.seeding_source
        obj['sourceID'] = self.source_id
        obj['topic'] = self.topic
        obj['content'] = collections.OrderedDict()
        for specialization_id in sorted(self.content.keys()):
            specialization_obj = self.content[specialization_id]
            if specialization_obj['values']:
                obj['content'][specialization_id] = self.content[specialization_id]

        return obj


    def set_id(self, prop_id):
        """Sets id of specialized property being edited.

        """
        self.content[prop_id] = self.content.get(prop_id, _NULL_PROPERTY())
        self._prop = self.content[prop_id]
        self._prop_specialization = get_property_specialization(prop_id)


    def set_value(self, val, val_parser=None):
        """Sets a scalar value.

        :param obj val: Value to be assigned.

        """
        # Validate input:
        # ... error if trying to add > 1 value to a property with singular cardinality.
        if not self._prop_specialization.is_collection and \
           len(self._prop['values']) >= 1:
            raise ValueError('Invalid property: only one value can be added')

        # ... error if adding a duplicate value.
        if val in self._prop['values']:
            raise ValueError('Invalid property: cannot add duplicate values')

        # ... error if specialization complains.
        self._prop_specialization.validate_value(val)

        # Apply parser (skip errors).
        if val_parser:
            try:
                val = val_parser(val)
            except:
                pass

        # Update state.
        self._prop['values'].append(val)


    def sort_values(self):
        """Sorts current property values.

        """
        self._prop['values'] = sorted(self._prop['values'])


    def get_values(self, specialization_id):
        """Returns a set of values.

        """
        return self.content.get(specialization_id, dict()).get('values', [])
