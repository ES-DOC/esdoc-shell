# -*- coding: utf-8 -*-

"""
.. module:: cv.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Wraps CMIP6 CV vocabulary validation.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import pyessv



def validate_vocabularies(projects, experiments):
    """Validate various CV termsets within collections.

    """
    _validate(
        'PROJECT',
        pyessv.load('wcrp:cmip6:activity-id'),
        projects
        )
    _validate(
        "EXPERIMENTS",
        pyessv.load('wcrp:cmip6:experiment-id'),
        experiments
        )
    print "------------------------------------------------------"


def _validate(typeof, terms, docs):
    """Inner function to perform the validation.

    """
    terms = sorted([i.name for i in terms])
    docs = sorted([i.name.lower() for i in docs])

    invalid_docs = [i for i in docs if i not in terms]
    if invalid_docs:
        print "------------------------------------------------------"
        print "INVALID {} SPREADSHEET NAMES".format(typeof)
        print "------------------------------------------------------"
        for doc in invalid_docs:
            print doc

    invalid_terms = [i for i in terms if i not in docs]
    if invalid_terms:
        print "------------------------------------------------------"
        print "UNMAPPED {} WCRP TERMS".format(typeof)
        print "------------------------------------------------------"
        for term in invalid_terms:
            print term
