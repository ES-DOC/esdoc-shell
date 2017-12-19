# -*- coding: utf-8 -*-

"""
.. module:: init_jhub_archive.__main__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initializes CMIP6 Jupyterhub archive.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import pyessv



# Set vocabs.
cmip6 = pyessv.vocabs.wcrp.cmip6

# Path to output file.
_FPATH = __file__.replace('__main__.py', 'output.txt')

_TEMPLATE = '''#!/bin/bash

# Import utils.
source $JH_ARCHIVE_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "initializing notebook archive ..."

{BASH}

    log "notebook archive initialized ..."
}

# Invoke entry point.
main
'''


def _main():
    """Main entry point.

    """
    commands = _get_commands()
    script = _TEMPLATE.replace('{BASH}', '\n'.join(commands))
    with open(_FPATH, 'w') as fstream:
        fstream.write(script)


def _get_commands():
    """Gets commands to be executed.

    """
    commands = []
    for i in cmip6.institution_id:
        for j in _get_sources(i):
            commands.append('\tsource $JH_ARCHIVE_HOME/sh/init_.sh cmip6 {} {}'.format(i.canonical_name, j.canonical_name))

    return commands


def _get_sources(institute):
    """Institute source identifiers.

    """
    def _is_related(source):
        return institute.canonical_name in [i.lower() for i in source.data['institution_id']]


    return [i for i in cmip6.source_id if _is_related(i)]


def _get_realms(source_id):
    """Source realms.

    """
    def _is_realized(realm):
        return source_id.data['model_component'][realm.raw_name]['description'] != 'none'

    return [i for i in cmip6.realm if _is_realized(i)]


# Entry point.
_main()
