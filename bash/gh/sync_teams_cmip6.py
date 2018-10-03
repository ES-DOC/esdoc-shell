# -*- coding: utf-8 -*-

"""
.. module:: sync_epos.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Synchronizes instituional repos.

.. moduleauthor:: Mark A. Conway-Greenslade


"""
import json
import os

import pyessv
import requests

import _utils as utils



def _main():
    """Main entry point.

    """
    # Set canonical institutes & actual GH teams.
    institutes = [i.canonical_name.split(':')[-1] for i in pyessv.load('wcrp:cmip6:institution-id')]
    teams = utils.get_teams(lambda i: i['name'].startswith('cmip6-'))

    # Set teams to be created.
    to_create = ['cmip6-{}'.format(i) for i in institutes if 'cmip6-{}'.format(i) not in teams]

    # Set teams to be deleted.
    to_delete = [i for i in teams.values() if i.name.startswith('cmip6') and  i.institution_id not in institutes]

    # Escape when nothing to do.
    if len(to_create) == 0 and len(to_delete) == 0:
        pyessv.log("Teams are in sync - nothing todo")
        return

    # Update GH.
    for team_id in to_create:
        utils.create_team(team_id)
    for team in to_delete:
        utils.delete_team(team)


# Main entry point.
if __name__ == '__main__':
    _main()
