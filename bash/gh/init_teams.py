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

import requests

import pyesdoc
import pyessv



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Initializes GitHub teams for user access control.")
_ARGS.add_argument(
    "--gh-user",
    help="An ES-DOC administrator GitHub user account",
    dest="gh_user",
    type=str
    )
_ARGS.add_argument(
    "--oauth-token",
    help="A GitHub OAuth personal access token",
    dest="oauth_token",
    type=str
    )
_ARGS.add_argument(
    "--gh-team",
    help="The GitHub team that the user wishes to have access to",
    dest="gh_team",
    type=str
    )

# GitHub API - user team membership within ES-DOC-OPS.
_GH_API_TEAMS = "https://api.github.com/orgs/ES-DOC-OPS/teams"


def _main(args):
	"""Main entry point.

	"""
	# Get list of WCRP sanctioned institute codes.
	institutes = pyessv.load('wcrp:cmip6:institution-id')

	# Set teams to be created.
	teams = {"{}-{}".format(args.gh_team, i.canonical_name) for i in institutes}
	teams.add(args.gh_team)

	# POST each new team to GH API
	for team in sorted(teams):
		# See - https://developer.github.com/v3/orgs/teams/#create-team
		r = requests.post(_GH_API_TEAMS,
			data=json.dumps({
				'maintainers': ['momipsl'],
				'name': team,
				'privacy': 'secret'
			}),
			headers={
				'Accept': "application/vnd.github.korra-preview+json"
			},
			auth=(args.gh_user, args.oauth_token)
			)

		# If created then log.
		if r.status_code == 201:
			pyesdoc.log("GitHub team created: {}".format(team))
			continue

		# If already exists then skip.
		elif r.status_code == 422:
			r = json.loads(r.text)
			if r['errors'][0]['code'] == u'already_exists':
				pyesdoc.log("GitHub team already exists: {}".format(team))
				continue

		# Otherwise log error.
		pyesdoc.log_error("GitHub team creation failed: {} :: {}".format(team, r.text))


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
