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
    institutes = _get_institutes()
    repos = utils.get_repos()

    repos_to_create = set(institutes).difference(set(repos.keys()))
    repos_to_delete = set(repos.keys()).difference(set(institutes))

    if len(repos_to_create) == 0 and len(repos_to_delete) == 0:
        pyessv.log("Repos are in sync - nothing todo")
        return

    for institution_id in repos_to_create:
        utils.create_repo(institution_id)

    for repo in [i for i in repos.values() if i.name in repos_to_delete]:
        utils.delete_repo(repo)


def _get_institutes():
    """Returns canonical cmip6 institutes (derived from vocabularies).

    """
    return [ i.canonical_name.split(':')[-1]
             for i in pyessv.load('wcrp:cmip6:institution-id') ]


# Main entry point.
if __name__ == '__main__':
    _main()
