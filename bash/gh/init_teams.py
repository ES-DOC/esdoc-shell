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
	# Set existing teams.
	teams = _get_teams()

	# Set institutes without a team.
	institutes = [i for i in pyessv.load('wcrp:cmip6:institution-id')
				  if _get_team_name(i) not in teams]

	# Create.
	for i in institutes:
		_create_team(i)


def _get_teams():
	"""Returns set of existing GH teams.

	"""
	url = '{}?per_page=100'.format(_GH_API_TEAMS)
	r = requests.get(url, auth=_GH_API_CREDENTIALS)

	return {i['name']: i for i in json.loads(r.text)}


def _get_team_name(institution):
	"""Returns GitHub team name for an institute.

	"""
	return 'staff-{}'.format(institution.canonical_name)


def _get_repo_name(institution):
	"""Returns GitHub repo name for an institute.

	"""
	return institution.canonical_name


def _create_team(institution):
	"""Creates an institutional GitHub team.

	"""
	# Post to GitHub API.
	team = _get_team_name(institution)
	payload = {
		'auto_init': True,
		'description': '{} staff members'.format(institution.canonical_name.upper()),
		'maintainers': [_GH_USER_NAME],
		'name': team,
		'privacy': 'secret',
		'repo_names': ['ES-DOC-INSTITUTIONAL/{}'.format(_get_repo_name(institution))]
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
