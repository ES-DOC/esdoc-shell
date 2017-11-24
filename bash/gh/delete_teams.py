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

# GitHub API - teams.
_GH_API_TEAMS_1 = "https://api.github.com/teams"

# Teams not to be deleted.
_EXCLUDED = {
	'cdf2cim-publication',
	'documentation-publication',
	'errata-publication'
	}


def _main():
	"""Main entry point.

	"""
	url = '{}?per_page=500'.format(_GH_API_TEAMS)
	r = requests.get(url, auth=_GH_API_CREDENTIALS)

	teams = []
	for team in json.loads(r.text):
		if team['name'] not in _EXCLUDED:
			teams.append((team['name'], team['id']))

	for name, identifier in teams:
		url = '{}/{}'.format(_GH_API_TEAMS_1, identifier)
		r = requests.delete(url, auth=_GH_API_CREDENTIALS)
		if r.status_code == 204:
			pyessv.log("GH-team deleted: {}".format(name), app='GH')
		else:
			pyessv.log_error("GH-team deletion failure: {} :: {}".format(name, r['errors'][0]['message']), app='GH')



# Main entry point.
if __name__ == '__main__':
    _main()