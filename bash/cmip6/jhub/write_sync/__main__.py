# -*- coding: utf-8 -*-

"""
.. module:: write_jhub_sync.__main__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Writes CMIP6 Jupyterhub sync script.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import pyessv



# Set vocabs.
cmip6 = pyessv.vocabs.wcrp.cmip6

# Path to output file.
_FPATH = __file__.replace('__main__.py', 'output.txt')

_TEMPLATE = '''#!/bin/bash

# Import utils.
source $JH_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "syncing notebook output ..."

{BASH}

    log "notebook output synced ..."
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
            commands.append('\tsource $JH_HOME/sh/sync_from_server_.sh cmip6 {} {}'.format(i.canonical_name, j.canonical_name))

    return commands


def _get_sources(institute):
    """Institute source identifiers.

    """
    def _is_related(source):
        return institute.canonical_name in [i.lower() for i in source.data['institution_id']]


    return [i for i in cmip6.source_id if _is_related(i)]


# Entry point.
_main()
