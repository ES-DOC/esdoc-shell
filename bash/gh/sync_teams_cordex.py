# -*- coding: utf-8 -*-

"""
.. module:: sync_teams_cordex.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Synchronizes CMIP5 teams.

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
    institutes = [i.canonical_name.split(':')[-1] for i in pyessv.load('wcrp:cordex:institution')]
    teams = utils.get_teams(lambda i: i['name'].startswith('cordex-'))

    # Set teams to be created.
    to_create = ['cordex-{}'.format(i) for i in institutes if 'cordex-{}'.format(i) not in teams]

    # Set teams to be deleted.
    to_delete = [i for i in teams.values() if i.name.startswith('cordex') and  i.institution_id not in institutes]

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
