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
    """Model topic documentation output wrapper.

    """
    def __init__(self, mip_era, institute, source_id, topic, path=None):
        """Instance initialiser.

        """
        self.authors = []
        self.contributors = []
        self.content = dict()
        self.fpath = path
        self.institute = unicode(institute).strip().lower()
        self.mip_era = unicode(mip_era).strip().lower()
        self.seeding_source = None
        self.source_id = unicode(source_id).strip().lower()
        self.specialization = get_topic_specialization(mip_era, topic)
        self.topic = unicode(topic).strip().lower()
        self._prop = None
        self._prop_specialization = None

        # Auto initialise from JSON output file.
        if os.path.isfile(self.fpath):
            with open(self.fpath, 'r') as fstream:
                self._from_dict(json.loads(fstream.read()))


    @classmethod
    def create(cls, m, i, s, t):
        """Get notebook output wrapper instance.

        :param str m: MIP era, e.g. cmip6.
        :param pyessv.Term i: Institute.
        :param pyessv.Term s: Model source.
        :param pyessv.Term t: Documentation topic.

        :returns: Model topic documentation output wrapper instance.
        :rtype: ModelTopicOutput

        """
        # Set path to JSON  file.
        name = get_file(m, i, s, t, 'json')
        path = get_folder((i, m, 'models', s, 'json'))
        path = os.path.join(path, name)

        # Return instance.
        return cls(m, i.canonical_name, s.canonical_name, t.canonical_name, path=path)


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
        self.authors = [(i['name'], i['email']) for i in obj['authors']]
        self.contributors = [(i['name'], i['email']) for i in obj['contributors']]
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
        obj['authors'] = [{'name': i[0], 'email': i[1]} for i in self.authors]
        obj['contributors'] = [{'name': i[0], 'email': i[1]} for i in self.contributors]
        obj['content'] = collections.OrderedDict()
        for specialization_id in sorted(self.content.keys()):
            specialization_obj = self.content[specialization_id]
            if specialization_obj['values']:
                obj['content'][specialization_id] = self.content[specialization_id]

        return obj


    def set_author(self, name, email):
        """Adds an author to managed collection.

        """
        # Format inputs.
        if name is not None:
            name = unicode(name).strip()
        if email is not None:
            email = unicode(email).strip()

        # Validate inputs.
        if name is None or len(name) == 0:
            raise ValueError('Invalid contributor name')
        if email is None or len(email) == 0:
            raise ValueError('Invalid contributor email')
        # TODO: validate with reg-ex.

        # Reject duplicates.
        for i, j in self.authors:
            if name.lower() == i.lower() and email.lower() == j.lower():
                return

        # Update state.
        self.authors.append((name, email))
        self.save()


    def set_contributor(self, name, email):
        """Adds a contributor to managed collection.

        """
        # Format inputs.
        if name is not None:
            name = unicode(name).strip()
        if email is not None:
            email = unicode(email).strip()

        # Validate inputs.
        if name is None or len(name) == 0:
            raise ValueError('Invalid contributor name')
        if email is None or len(email) == 0:
            raise ValueError('Invalid contributor email')
        # TODO: validate with reg-ex.

        # Reject duplicates.
        for i, j in self.contributors:
            if name.lower() == i.lower() and email.lower() == j.lower():
                return

        # Update state.
        self.contributors.append((name, email))
        self.save()


    def set_id(self, prop_id):
        """Sets id of specialized property being edited.

        """
        self.content[prop_id] = self.content.get(prop_id, _NULL_PROPERTY())
        self._prop = self.content[prop_id]
        self._prop_specialization = get_property_specialization(prop_id)


    def set_value(self, val):
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


    def get_comma_delimited_values(self, specialization_id):
        """Returns a set of comma delimited values.

        """
        value = self.get_value(specialization_id)

        return [i.trim() for i in value.split(',')] if value else []


    def get_value(self, specialization_id):
        """Returns a single value.

        """
        values = self.get_values(specialization_id)

        return values[0] if values else None


def get_folder(parts):
    """Returns path to an institute's mip-era repository.

    """
    path = os.path.join(os.getenv('ESDOC_HOME'), 'repos')
    path = os.path.join(path, 'institutional')
    for part in parts:
        if part is None:
            continue
        try:
            part.canonical_name
        except AttributeError:
            path = os.path.join(path, part)
        else:
            path = os.path.join(path, part.canonical_name)
    if not os.path.isdir(path):
        os.makedirs(path)

    return path


def get_folder_of_cmip6_institute(i):
    """Returns path to an institute's repository for a particular model/source.

    """
    return get_folder((i, 'cmip6', 'models'))


def get_folder_of_cmip6_source(i, s, subfolder=None):
    """Returns path to an institute's repository for a particular model/source.

    """
    return get_folder((i, 'cmip6', 'models', s, subfolder))


def get_file(m, i, s, t, encoding):
    """Returns a file name.

    """
    if t is not None:
        return '{}_{}_{}_{}.{}'.format(m, i.canonical_name, s.canonical_name, t.canonical_name, encoding)    
    return '{}_{}_{}.{}'.format(m, i.canonical_name, s.canonical_name, encoding)


def get_file_of_cmip6(i, s, t, encoding):
    """Returns a cmip6 file name.

    """
    return get_file('cmip6', i, s, t, encoding)
