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

# Project configuration.
_CONFIG = {
	('cmip5', 'wcrp:cmip5:institute'),
	('cmip6', 'wcrp:cmip6:institution-id'),
	('cordex', 'wcrp:cordex:institute')
}



def _main():
	"""Main entry point.

	"""
	existing_teams = _get_teams()
	for project, collection_id in _CONFIG:
		institutes = pyessv.load(collection_id)
		for institute in institutes:
			team = '{}-{}'.format(project, institute.canonical_name)
			if team not in existing_teams:
				_create_team1(project, institute.canonical_name, team)


def _get_teams():
	"""Returns set of existing GH teams.

	"""
	url = '{}?per_page=500'.format(_GH_API_TEAMS)
	r = requests.get(url, auth=_GH_API_CREDENTIALS)

	return [i['name'] for i in json.loads(r.text)]


def _create_team1(project, institute, team):
	"""Creates an institutional GitHub team.

	"""
	# Post to GitHub API.
	payload = {
		'auto_init': True,
		'description': '{} project {} team'.format(project.upper(), institute.upper()),
		'maintainers': [_GH_USER_NAME],
		'name': team,
		'privacy': 'secret'
	}
	r = requests.post(_GH_API_TEAMS,
		data=json.dumps(payload),
		headers={
			'Accept': "application/vnd.github.korra-preview+json"
		},
		auth=_GH_API_CREDENTIALS
		)

	# If created then log.
	if r.status_code == 201:
		pyessv.log("GH-team created: {}".format(team), app='GH')

	# If already exists then skip.
	elif r.status_code == 422:
		pyessv.log("GH-team already exists: {}".format(team), app='GH')

	# Otherwise log error.
	else:
		pyessv.log_error("GH-team creation failure: {} :: {}".format(team, r['errors'][0]['message']), app='GH')


# Main entry point.
if __name__ == '__main__':
    _main()
