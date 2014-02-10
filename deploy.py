#! /usr/bin/python
"""
    esdoc_deploy_0.py
    ~~~~~~~~~~~

    Executes full ESDOC stack deployment to webfactional server.

    :copyright: (c) 2013 by ES-DOCumentation.

"""
import shutil
import subprocess
import sys
import xmlrpclib
from os.path import abspath, join, dirname


# Web faction api url.
_WEB_FACTION_API_URL = 'https://api.webfaction.com/'

# Web faction api user id.
_WEB_FACTION_API_USER_ID = 'esdoc'

# ESDOC stack (type, subtype, name).
_STACK = [
    ('app', 'mod_wsgi33-python26', 'api'),
    ('app', 'static_only', 'splash'),
    ('app', 'static_only', 'static'),
    ('app', 'static_only', 'compare'),
    ('app', 'static_only', 'search'),
    ('app', 'static_only', 'view'),
    ('app', 'static_only', 'visualize'),
    ('db', 'postgresql', 'api')
]

# Shell root directory.
_dir = dirname(abspath(__file__))

# Home directory.
_dir_home = dirname(_dir)

# Webapps directory.
_dir_webapps = join(_dir_home, "webapps")

# Git repos directory.
_dir_repos = join(_dir, "repos")

# DB backups directory.
_dir_db_backups = join(join(_dir, "db"), "backups")

# Map of repos and associated directories.
_source = {
    "splash": join(_dir_repos, "esdoc-splash/src"),
    "static": join(_dir_repos, "esdoc-static"),
    "compare": join(_dir_repos, "esdoc-js-client/demo"),
    "visualize": join(_dir_repos, "esdoc-js-client/demo"),
    "search": join(_dir_repos, "esdoc-js-client/demo"),
    "view": join(_dir_repos, "esdoc-js-client/demo"),
}


class DeploymentContext(object):
    """Encapsulates deployment contextual information.

    """
    def __init__(self, argv):
        self.environment = argv[0]
        self.version = argv[1]
        self.wf_machine = argv[2]
        self.wf_pwd = argv[3]
        self.api_db_pwd = argv[4]

        self.id = self.version.replace('.', '_')
        self.api_port = str(0)
        self._webapp_name_format = self.environment + "_{0}_" + self.id

        _log(self)


    def __str__(self):
        result = "env: "
        result += str(self.environment)
        result += " | version: "
        result += str(self.version)
        result += " | id: "
        result += str(self.id)
        result += " | wf-machine: "
        result += str(self.wf_machine)
        result += " | wf pwd: "
        result += str(self.wf_pwd)
        result += " | db pwd: "
        result += str(self.api_db_pwd)
        
        return result


    def get_webapp_name(self, name):
        return self._webapp_name_format.format(name)


    def get_webapp_dir(self, name):
        return join(_dir_webapps, self.get_webapp_name(name))


class DeploymentError(Exception):
    """Encapsulates deployment error information.

    """
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


class StackElement(object):
    """Encapsulates information related to a stack element.

    """
    def __init__(self, ctx, config):
        self.type = config[0]
        self.subtype = config[1]
        self.name = StackElement.get_name(ctx, config[2])
        self.website = StackElement.get_website_name(ctx, config[2])


    @staticmethod
    def get_name(ctx, element):
        """Returns ESDOC webfaction application stack element name.

        :param ctx: Deployment context information.
        :type ctx: DeploymentContext

        :param element: Stack element name.
        :type element: str

        :return: Full stack element name.
        :rtype: str

        """
        return ctx.environment + '_' + ctx.id + '_' + element


    @staticmethod
    def get_website_name(ctx, element):
        """Returns ESDOC webfaction application stack website name.

        :param ctx: Deployment context information.
        :type ctx: DeploymentContext

        :param element: Stack element name.
        :type element: str

        :return: Full stack website name.
        :rtype: str

        """
        return ctx.environment + '_' + element



def _log(msg, tabs=0):
    for i in range(tabs):
        msg = "\t" + msg
    print "ESDOC - DEPLOY: {0}".format(msg)


def _get_filepath(fname, parent=False):
    """Returns the path to a sub-script."""
    fpath = _dir_home if parent else _dir

    return join(fpath, fname)


# Path to exec file.
_EXEC = _get_filepath("exec.sh")


# Path to deploy file.
_DEPLOY = _get_filepath("deploy.sh")


def _get_repo(name):
    return join(_dir_repos, name)


def _declare_stack(ctx):
    """Sets the ESDOC webfaction application stack list."""
    ctx.wf_stack = [StackElement(ctx, i) for i in _STACK]


def _set_wf_session(ctx):
    """Sets the webfactional server session."""
    ctx.wf = xmlrpclib.ServerProxy(_WEB_FACTION_API_URL)
    ctx.wf_session, ctx.wf_account = ctx.wf.login(_WEB_FACTION_API_USER_ID, \
                                                  ctx.wf_pwd, \
                                                  ctx.wf_machine)
    _refresh_wf_session(ctx)


def _refresh_wf_session(ctx):
    """Refreshes the webfactional server session."""
    ctx.wf_app_list = {}
    for i in ctx.wf.list_apps(ctx.wf_session):
        ctx.wf_app_list[i['name']] = i
    ctx.wf_website_list = {}
    for i in ctx.wf.list_websites(ctx.wf_session):
        ctx.wf_website_list[i['name']] = i


def _set_api_port(ctx):
    """Assigns the ESDOC api webfaction port number stack."""
    api = StackElement.get_name(ctx, 'api')
    ctx.api_port = str(ctx.wf_app_list[api]['port'])


def _create_wf_dbs(ctx):
    """Creates ESDOC databases upon target webfactional server."""
    for el in [i for i in ctx.wf_stack if i.type == 'db']:
        try:
            ctx.wf.create_db(ctx.wf_session, el.name, el.subtype, ctx.api_db_pwd)
        except:
            _log('... failure when creating db : ' + el.name)
        else:
            _log('... created db : ' + el.name)


def _create_wf_apps(ctx):
    """Creates ESDOC apps upon target webfactional server."""
    for el in [i for i in ctx.wf_stack if i.type == 'app']:
        try:
            ctx.wf.create_app(ctx.wf_session, el.name, el.subtype, False, '')
        except:
            _log('... failure when creating app : ' + el.name)
        else:
            _log('... created app : ' + el.name)


def _delete_wf_dbs(ctx):
    """Deletes ESDOC databases from target webfactional server."""
    for el in [i for i in ctx.wf_stack if i.type == 'db']:
        # ... delete db.
        try:
            ctx.wf.delete_db(ctx.wf_session, el.name, el.subtype)
        except:
            _log('... failure when deleting db : ' + el.name)
        else:
            _log('... deleted db : ' + el.name)

        # ... delete db user.
        try:
            ctx.wf.delete_db_user(ctx.wf_session, el.name, el.subtype)
        except:
            _log('... failure when deleting db user : ' + el.name)
        else:
            _log('... deleted db user : ' + el.name)


def _delete_wf_apps(ctx):
    """Deletes ESDOC apps from target webfactional server."""
    for el in [i for i in ctx.wf_stack if i.type == 'app']:
        try:
            ctx.wf.delete_app(ctx.wf_session, el.name)
        except:
            _log('... failure when deleting app : ' + el.name)
        else:
            _log('... deleted app : ' + el.name)


def _update_wf_websites(ctx):
    """Updates the wf websites so that they point to the correct application."""
    def update_website(ws, app=None):
        ws['website_apps'] = [] if app is None else [[app, '/']]
        ctx.wf.update_website(ctx.wf_session,
                              ws['name'],
                              ws['ip'],
                              ws['https'],
                              ws['subdomains'],
                              *ws['website_apps'])

    # For each app updated the associated website.
    for i in [i for i in ctx.wf_stack if i.type == 'app']:
        print "AAA", i.website
    print ctx.wf_website_list

    return

    for el in [i for i in ctx.wf_stack if i.type == 'app' and i.website in ctx.wf_website_list]:
        ws = ctx.wf_website_list[el.website]
        update_website(ws)
        update_website(ws, el.name)

        _log('... updated website ' + el.website + ' to point towards ' + el.name)


def _update_repos(ctx):
    """Updates source code repositories."""
    subprocess.call([_EXEC, "_update_repos"])
    

def _install_source(ctx):
    """Installs source code."""
    subprocess.call([_DEPLOY, "install_source", ctx.environment, ctx.id])


def _restore_db(ctx):
    """Installs databases from backups."""
    subprocess.call([_DEPLOY, "restore_db", ctx.environment, ctx.id, ctx.api_db_pwd])


def _restart_services(ctx):
    """Restarts application services."""
    subprocess.call([_DEPLOY, "restart_services", ctx.environment, ctx.id])


def _stop_services(ctx):
    """Stops application services."""
    subprocess.call([_DEPLOY, "stop_services", ctx.environment, ctx.id])


# Set of actions.
_actions = {
    'rollout' : [
        (_declare_stack, "Declaring stack"),
        (_set_wf_session, "Initialising web faction session"),
        (_create_wf_apps, "Creating apps upon web faction server"),
        (_create_wf_dbs, "Creating databases upon web faction server"),
        (_refresh_wf_session, "Refreshing web faction session"),
        (_set_api_port, "Assigning API port"),
        # (_update_repos, "Updating repositories"),
        # (_install_source, "Installing source(s)"),
        # (_restore_db, "Restoring database(s)"),
        # (_restart_services, "Restarting services"),
        (_update_wf_websites, "Updating web faction websites")
    ],
    'rollback' : [
        (_declare_stack, "Declaring stack"),
        (_set_wf_session, "Initialising web faction session"),
        # (_stop_services, "Stopping services"),
        (_delete_wf_apps, "Deleting apps from web faction server"),
        (_delete_wf_dbs, "Deleting databases from web faction server")
    ]
}

if __name__ == "__main__":
    """Main entry point.

    """
    if sys.argv[1] not in _actions:
        raise DeploymentError("Deployment method unrecognised.")

    # Instantiate context.
    ctx = DeploymentContext(sys.argv[2:])

    # Execute actions.
    for index, action_info in enumerate(_actions[sys.argv[1]]):
        _log("Step " + str(index) + ". " + action_info[1])
        action_info[0](ctx)
