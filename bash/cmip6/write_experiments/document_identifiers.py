# -*- coding: utf-8 -*-

"""
.. module:: document_identifiers.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Loads static document identifiers from file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import collections
import uuid



class DocumentIdentifiers(object):
    """Wraps set of static document identifiers.

    """
    def __init__(self, fpath):
        """Instance constructor.

        """
        self._uids = collections.defaultdict(lambda: collections.defaultdict(int))
        with open(fpath, 'r') as fstream:
            for line in fstream.readlines():
                ws_name, ws_row, doc_uid = line.split("::")
                self._uids[ws_name][ws_row] = uuid.UUID(doc_uid.replace("\n", ""))


    def __getitem__(self, ws_name):
        """Returns identifier collection.

        """
        return self._uids[ws_name]
