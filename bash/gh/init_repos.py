# -*- coding: utf-8 -*-

"""
.. module:: init_gh_team.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initializes an ES-DOC-OPS GitHub user team.

.. moduleauthor:: Mark A. Conway-Greenslade


"""
import argparse
import json
import os

import requests

import pyessv



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Initializes GitHub repos for institutional control.")

# GitHub - user name.
_GH_USER_NAME = 'esdoc-system-user'

# GitHub - access token.
_GH_ACCESS_TOKEN = os.getenv('ESDOC_GITHUB_ACCESS_TOKEN')

# GitHub API - create repo.
_GH_API_REPO_CREATE = "https://api.github.com/orgs/ES-DOC-INSTITUTIONAL/repos"



def _main(args):
	"""Main entry point.

	"""
	# Get list of WCRP sanctioned institute codes.
	institutes = pyessv.load('wcrp:cmip6:institution-id')

	# Set repos to be created.
	for i in institutes:
		repo = i.canonical_name

		payload = {
			'auto_init': True,
			'name': repo,
			'description': '{} documentation archive'.format(repo.upper()),
			'homepage': 'https://github.com/ES-DOC-INSTITUTIONAL/{}'.format(repo),
			'private': False,
			'license_template': 'gpl-3.0',
			'has_issues': True,
			'has_projects': True,
			'has_wiki': True
		}
		r = requests.post(_GH_API_REPO_CREATE,
			data=json.dumps(payload),
			headers={
				'Accept': "application/vnd.github.korra-preview+json"
			},
			auth=(_GH_USER_NAME, _GH_ACCESS_TOKEN)
			)

		# If created then log.
		if r.status_code == 201:
			pyessv.log("GH-repo created: {}".format(repo))

		# If already exists then skip.
		elif r.status_code == 422:
			pyessv.log("GH-repo already exists: {}".format(repo))

		# Otherwise log error.
		else:
			pyessv.log_error("GH-repo creation failure: {} :: {}".format(repo, r['errors'][0]['message']))


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
