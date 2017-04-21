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

import pyesdoc
import pyessv



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Initializes GitHub repos for institutional control.")

# GitHub - user name.
_GH_USER_NAME = 'esdoc-system-user'

# GitHub - access token.
_GH_ACCESS_TOKEN = os.getenv('ESDOC_GITHUB_ACCESS_TOKEN')

# GitHub API - create repo.
_GH_API_REPO_CREATE = "https://api.github.com/orgs/ES-DOC-CMIP6/repos"

# GitHub API - delete repo.
_GH_API_REPO_DELETE = "https://api.github.com/repos/ES-DOC-CMIP6/{}"



def _main(args):
	"""Main entry point.

	"""
	# Get list of WCRP sanctioned institute codes.
	institutes = pyessv.load('wcrp', 'cmip6', 'institution-id')

	# _create_repos(institutes)
	_delete_repos(institutes)


def _create_repos(institutes):
	"""Creates repos in question.

	"""
	# Set repos to be created.
	for i in institutes:
		repo = 'esdoc-{}'.format(i.name)
		payload = {
			'auto_init': True,
			'name': repo,
			'description': '{} CMIP6 documentation archive'.format(i.name.upper()),
			'homepage': 'https://github.com/ES-DOC-CMIP6/{}'.format(repo),
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
			pyesdoc.log("GH-repo created: {}".format(repo))

		# If already exists then skip.
		elif r.status_code == 422:
			pyesdoc.log("GH-repo already exists: {}".format(repo))

		# Otherwise log error.
		else:
			pyesdoc.log_error("GH-repo creation failure: {} :: {}".format(repo, r['errors'][0]['message']))

		break


def _delete_repos(institutes):
	"""Deletes repos in question.

	"""
	for i in institutes:
		repo = 'esdoc-cmip6-{}'.format(i.name)
		ep = _GH_API_REPO_DELETE.format(repo)

		print ep
		r = requests.delete(_GH_API_REPO_DELETE.format(repo),
			auth=(_GH_USER_NAME, _GH_ACCESS_TOKEN)
			)
		print r.status_code

		break

# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
