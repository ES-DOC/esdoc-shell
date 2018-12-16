# -*- coding: utf-8 -*-

"""
.. module:: init_settings.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initializes CMIP6 model settings files.

.. moduleauthor:: Mark A. Conway-Greenslade


"""
import argparse
import collections
import json
import os

import pyessv



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Generates CMIP6 model setting files.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str,
    default="all"
    )


def _main(args):
    """Main entry point.

    """
    # Set writers to be executed.
    writers = [
        InitialisationFromCmip5ModelSettings,
        ModelPublicationSettings
        ]

    # Set institutes to be processed.
    institutes = pyessv.WCRP.cmip6.institution_id if args.institution_id == 'all' else \
                 [pyessv.WCRP.cmip6.institution_id[args.institution_id]]

    # Write a settings file CMIP6 institute | setting combination.
    for i in institutes:
        for writer in [w(i) for w in writers]:
            writer.execute()


class ModelSettings(object):
    def __init__(self, institution, fname):
        """Ctor.

        """
        self.directory = None
        self.fname = fname
        self.institution = institution
        self.new = collections.OrderedDict()
        self.previous = None


    def execute(self):
        self._set_directory()
        self._set_previous_settings()
        self._set_new_settings()
        self._write()


    def _get_topics(self, source):
        """Returns set of topics to be processed.

        """
        return [pyessv.ESDOC.cmip6.model_topic.toplevel] + \
                pyessv.WCRP.cmip6.get_source_realms(source)


    def _set_directory(self):
        """Assigns directory path.

        """
        fpath = os.getenv('ESDOC_HOME')
        fpath = os.path.join(fpath, 'repos')
        fpath = os.path.join(fpath, 'institutional')
        fpath = os.path.join(fpath, self.institution.canonical_name)
        if not os.path.isdir(fpath):
            raise ValueError('{} GitHub repo does not exist.'.format(self.institution.canonical_name))
        fpath = os.path.join(fpath, 'cmip6')
        fpath = os.path.join(fpath, 'models')
        if not os.path.isdir(fpath):
            os.makedirs(fpath)

        self.directory = fpath


    def _set_new_settings(self):
        """Assigns new settings.

        """
        for source in pyessv.WCRP.cmip6.get_institute_sources(self.institution):
            settings = collections.OrderedDict()
            for realm in self._get_topics(source):
                settings[realm.canonical_name] = self._get_new_setting(source, realm)
            self.new[source.canonical_name] = settings


    def _set_previous_settings(self):
        """Assigns previous settings.

        """
        fpath = os.path.join(self.directory, self.fname)
        if os.path.exists(fpath):
            with open(fpath, 'r') as fstream:
                self.previous = json.loads(fstream.read())


    def _write(self):
        """Writes settings to file system.

        """
        fpath = os.path.join(self.directory, self.fname)
        with open(fpath, 'w') as fstream:
            fstream.write(json.dumps(self.new, indent=4))


class InitialisationFromCmip5ModelSettings(ModelSettings):
    """Encpasulates initialisation settings drawn from CMIP5.

    """
    def __init__(self, institution):
        """Ctor.

        """
        super(InitialisationFromCmip5ModelSettings, self).__init__(institution, 'initialization_from_CMIP5.json')


    def _get_new_setting(self, source, realm):
        """Returns a new setting to be written to fs.

        """
        def get_initialized_from():
            try:
                return self.previous[source.canonical_name][realm.canonical_name]['initializedFrom']
            except (TypeError, KeyError) as err:
                return ""

        return {
            "initializedFrom": get_initialized_from()
        }


class ModelPublicationSettings(ModelSettings):
    """Encpasulates model publication settings.

    """
    def __init__(self, institution):
        """Ctor.

        """
        super(ModelPublicationSettings, self).__init__(institution, 'model_publication.json')


    def _get_new_setting(self, source, realm):
        """Returns a new setting to be written to fs.

        """
        def get_publish_state():
            try:
                return self.previous[source.canonical_name][realm.canonical_name]['publish']
            except (TypeError, KeyError) as err:
                return "off"

        return {
            "publish": get_publish_state()
        }



# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
