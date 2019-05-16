import json
import os

import requests

import pyessv



# GitHub - user name.
GH_USER_NAME = 'esdoc-system-user'

# GitHub - access token.
GH_ACCESS_TOKEN = os.getenv('ESDOC_GITHUB_ACCESS_TOKEN')

# GitHub API - credentials.
GH_API_CREDENTIALS = (GH_USER_NAME, GH_ACCESS_TOKEN)

# GitHub API - organizational repos.
GH_API_ORG_REPOS = "https://api.github.com/orgs/ES-DOC-INSTITUTIONAL/repos"

# GitHub API - organizational teams.
GH_API_ORG_TEAMS = "https://api.github.com/orgs/ES-DOC-INSTITUTIONAL/teams"

# GitHub API - all teams.
GH_API_TEAMS = "https://api.github.com/teams"


def create_repo(institution_id):
    """Create a new institutional repo.

    """
    # Set payload.
    data = json.dumps({
        'auto_init': True,
        'name': institution_id,
        'description': '{} documentation archive'.format(institution_id.upper()),
        'homepage': 'https://github.com/ES-DOC-INSTITUTIONAL/{}'.format(institution_id),
        'private': False,
        'license_template': 'gpl-3.0',
        'has_issues': True,
        'has_projects': True,
        'has_wiki': True
    })

    # Post to Gh api.
    r = requests.post(GH_API_ORG_REPOS, data=data, auth=GH_API_CREDENTIALS)

    # If created then log.
    if r.status_code == 201:
        pyessv.log("GH-repo created: {}".format(institution_id))

    # If already exists then skip.
    elif r.status_code == 422:
        pyessv.log("GH-repo already exists: {}".format(institution_id))

    # Otherwise log error.
    else:
        pyessv.log_error("GH-repo creation failure: {} :: {}".format(institution_id, r['errors'][0]['message']))


def create_team(team_id):
    """Creates an institutional GitHub team.

    """
    # Post to GitHub API.
    payload = {
        'auto_init': True,
        'description': '{} team'.format(team_id.upper()),
        'maintainers': [GH_USER_NAME],
        'name': team_id,
        'privacy': 'secret'
    }

    r = requests.post(GH_API_ORG_TEAMS,
        data=json.dumps(payload),
        auth=GH_API_CREDENTIALS
        )

    # If created then log.
    if r.status_code == 201:
        pyessv.log("GH-team created: {}".format(team_id), app='GH')

    # If already exists then skip.
    elif r.status_code == 422:
        pyessv.log("GH-team already exists: {}".format(team_id), app='GH')

    # Otherwise log error.
    else:
        pyessv.log_error("GH-team creation failure: {} :: {}".format(team_id, r['errors'][0]['message']), app='GH')


def delete_repo(repo):
    """Informs user of required deltions to be manually performed.

    """
    pyessv.log("TODO: manually delete GitHub repo: {}".format(repo.name))


def delete_team(team):
    """Informs user of required deltions to be manually performed.

    """
    pyessv.log("TODO: manually delete GitHub team: {}".format(team.name))


def _get_entities(endpoint, predicate, entities):
    """Returns paged entities from GH api.

    """
    r = requests.get(endpoint, auth=GH_API_CREDENTIALS)
    data = json.loads(r.text)
    entities += data if predicate is None else [i for i in data if predicate(i)]
    if r.links.get('next', None):
        _get_entities(r.links['next']['url'], predicate, entities)


def get_teams(predicate=None):
    """Returns map of GitHub teams.

    """
    endpoint = '{}?per_page=100&page=1'.format(GH_API_ORG_TEAMS)
    entities = []
    _get_entities(endpoint, predicate, entities)

    return {i['name']: GitHubTeam(i) for i in entities}


def get_repos(predicate=None):
    """Returns map of GitHub repos.

    """
    endpoint = '{}?per_page=100'.format(GH_API_ORG_REPOS)
    entities = []
    _get_entities(endpoint, predicate, entities)

    return {i['name']: GitHubRepo(i) for i in entities}


class GitHubRepo(object):
    def __init__(self, obj):
        self.gh_id = obj['id']
        self.name = obj['name']
        self.obj = obj
        self.typeof = 'repo'
        self.institution_id = self.name

    def __repr__(self):
        return '{} :: {} :: {}'.format(self.typeof, self.name, self.gh_id)


class GitHubTeam(object):
    def __init__(self, obj):
        self.gh_id = obj['id']
        self.institution_id = obj['name'][6:]
        self.mip_era = obj['name'][0:5]
        self.name = obj['name']
        self.obj = obj
        self.typeof = 'team'

    def __repr__(self):
        return '{} :: {} :: {} :: {}'.format(self.typeof, self.name, self.gh_id, self.institution_id)
