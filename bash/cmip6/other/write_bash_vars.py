    # -*- coding: utf-8 -*-

"""
.. module:: write_bash_vars.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps raw WCRP CMIP6 vocab files to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import json
import os

import arrow

import pyessv



# Map of CMIP6 collections to data factories / name pre-formatters.
_VOCABS = {
    'cmip6': {
        'activity_id',
        'experiment_id',
        'institution_id',
        'source_id'
        },
    'global': {
        'mip_era'
    }
}

# Template input file.
_TEMPLATE = __file__.replace('.py', '_template.txt')

# Output file.
_OUTPUT = __file__.replace('.py', '_output.sh')



def _main():
    """Main entry point.

    """
    # Open template.
    with open(_TEMPLATE, 'r') as fstream:
        content = fstream.read()

    # Create CMIP6 collections.
    for scope in _VOCABS:
        for collection in [pyessv.load('wcrp:{}:{}'.format(scope, i)) for i in _VOCABS[scope]]:
            data = ''
            for term in collection:
                data += '\t\'{}\'\n'.format(term.canonical_name)
            content = content.replace('[{}]'.format(collection.raw_name.upper()), data)

            data = ''
            for term in collection:
                data += '\t\'{}\'\n'.format(term.raw_name)
            content = content.replace('[{}_RAW]'.format(collection.raw_name.upper()), data)

    # Write output to file system.
    with open(_OUTPUT, 'w') as fstream:
        fstream.write(content)


# Entry point.
if __name__ == '__main__':
    _main()
