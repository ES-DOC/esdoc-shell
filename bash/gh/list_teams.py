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

import requests

import pyessv



# GitHub - user name.
_GH_USER_NAME = 'esdoc-system-user'

# GitHub - access token.
_GH_ACCESS_TOKEN = os.getenv('ESDOC_GITHUB_ACCESS_TOKEN')

# GitHub API - credentials.
_GH_API_CREDENTIALS = (_GH_USER_NAME, _GH_ACCESS_TOKEN)

# GitHub API - teams.
_GH_API_TEAMS = "https://api.github.com/orgs/ES-DOC-INSTITUTIONAL/teams"


def _main():
	"""Main entry point.

	"""
	url = '{}?per_page=100'.format(_GH_API_TEAMS)
	r = requests.get(url, auth=_GH_API_CREDENTIALS)

	for team in json.loads(r.text):
		print "\t'{}': {},".format(team['name'], team['id'])


# Main entry point.
if __name__ == '__main__':
    _main()
