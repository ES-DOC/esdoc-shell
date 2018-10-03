# -*- coding: utf-8 -*-

"""
.. module:: init_gh_team.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initializes an ES-DOC-OPS GitHub user team.

.. moduleauthor:: Mark A. Conway-Greenslade


"""
import json
import os

import pyessv
import requests

import _utils as utils



# Teams not to be deleted.
_EXCLUDED = {
	'cdf2cim-publication',
	'documentation-publication',
	'errata-publication'
	}


def _main():
	"""Main entry point.

	"""
	teams = utils.get_teams()
	teams = [i for i in teams.values() if i.name not in _EXCLUDED]
	for team in teams:
		utils.delete_team(team.gh_id)


# Main entry point.
if __name__ == '__main__':
    _main()