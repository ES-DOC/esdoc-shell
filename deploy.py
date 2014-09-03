#! /usr/bin/python
"""
.. module:: deploy.py
   :copyright: @2013 Earth System Documentation (http://es-doc.org)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: ES-DOC webfaction delpoyment.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import subprocess, sys, xmlrpclib
from os.path import abspath, join, dirname


# Web faction api url.
_WEB_FACTION_API_URL = 'https://api.webfaction.com/'

# Web faction api user id.
_WEB_FACTION_API_USER_ID = 'esdoc'

# ESDOC stack (type, subtype, name).
_STACK = [
    ('app', 'custom_app_with_port', 'api'),
    ('app', 'static_only', 'splash'),
    ('app', 'static_only', 'static'),
    ('app', 'static_only', 'compare'),
    ('app', 'static_only', 'search'),
    ('app', 'static_only', 'view'),
    ('app', 'static_only', 'demo'),
    ('app', 'static_only', 'visualize'),
    ('db', 'postgresql', 'api')
]

# Shell root directory.
_DIR = dirname(abspath(__file__))

# Home directory.
_DIR_ESDOC_HOME = dirname(_DIR)

# Webapps directory.
_DIR_WEBAPPS = join(_DIR_ESDOC_HOME, "webapps")

# Path to exec.sh.
_EXEC = join(_DIR, "exec.sh")

# Path to deploy.sh.
_DEPLOY = join(_DIR, "deploy.sh")


class DeploymentContext(object):
    """Encapsulates deployment contextual information.

    """
    def __init__(self, environment, version, wf_machine, wf_pwd, api_db_pwd):
        """Object ctor."""
        self.environment = environment
        self.version = version
        self.wf_machine = wf_machine
        self.wf_pwd = wf_pwd
        self.api_db_pwd = api_db_pwd

        self.release_id = self.version.replace('.', '_')
        self.api_port = str(0)
        self._webapp_name_format = self.environment + "_{0}_" + self.release_id

        _log(self)


    def __str__(self):
        """Object string representation."""
        result = "env: "
        result += str(self.environment)
        result += " | version: "
        result += str(self.version)
        result += " | id: "
        result += str(self.release_id)
        result += " | wf-machine: "
        result += str(self.wf_machine)
        result += " | wf pwd: "
        result += str(self.wf_pwd)
        result += " | db pwd: "
        result += str(self.api_db_pwd)

        return result


    def get_webapp_name(self, name):
        """Returns web application name."""
        return self._webapp_name_format.format(name)


    def get_webapp_dir(self, name):
        """Returns web application directory."""
        return join(_DIR_WEBAPPS, self.get_webapp_name(name))


class DeploymentError(Exception):
    """Encapsulates deployment error information.

    """
    def __init__(self, error):
        """Object ctor."""
        self.error = error

    def __str__(self):
        """Object string representation."""
        return self.error


class StackElement(object):
    """Encapsulates information related to a stack element.

    """
    def __init__(self, ctx, config):
        """Object ctor."""
        self.type = config[0]
        self.subtype = config[1]
        self.name = StackElement.get_name(ctx, config[2])
        self.website = StackElement.get_website_name(ctx, config[2])


    @staticmethod
    def get_name(ctx, element):
        """Returns ESDOC webfaction application stack element name."""
        return "{0}_{1}_{2}".format(ctx.environment, ctx.release_id, element)


    @staticmethod
    def get_website_name(ctx, element):
        """Returns ESDOC webfaction application stack website name."""
        return "{0}_{1}".format(ctx.environment, element)


def _log(msg, tabs=0):
    """Outpus a message to logging."""
    for _ in range(tabs):
        msg = "\t" + msg
    print "ESDOC - DEPLOY: {0}".format(msg)


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
    for elem in [i for i in ctx.wf_stack if i.type == 'db']:
        try:
            ctx.wf.create_db(ctx.wf_session,
                             elem.name,
                             elem.subtype,
                             ctx.api_db_pwd)
        except Exception as exc:
            _log('... failure when creating db : ' + elem.name)
            raise exc
        else:
            _log('... created db : ' + elem.name)


def _create_wf_apps(ctx):
    """Creates ESDOC apps upon target webfactional server."""
    for elem in [i for i in ctx.wf_stack if i.type == 'app']:
        try:
            ctx.wf.create_app(ctx.wf_session,
                              elem.name,
                              elem.subtype,
                              False,
                              '')
        except Exception as exc:
            _log('... failure when creating app : ' + elem.name)
            raise exc
        else:
            _log('... created app : ' + elem.name)


def _delete_wf_dbs(ctx):
    """Deletes ESDOC databases from target webfactional server."""
    for elem in [i for i in ctx.wf_stack if i.type == 'db']:
        # ... delete db.
        try:
            ctx.wf.delete_db(ctx.wf_session, elem.name, elem.subtype)
        except:
            _log('... failure when deleting db : ' + elem.name)
        else:
            _log('... deleted db : ' + elem.name)

        # ... delete db user.
        try:
            ctx.wf.delete_db_user(ctx.wf_session, elem.name, elem.subtype)
        except:
            _log('... failure when deleting db user : ' + elem.name)
        else:
            _log('... deleted db user : ' + elem.name)


def _delete_wf_apps(ctx):
    """Deletes ESDOC apps from target webfactional server."""
    for elem in [i for i in ctx.wf_stack if i.type == 'app']:
        try:
            ctx.wf.delete_app(ctx.wf_session, elem.name)
        except:
            _log('... failure when deleting app : ' + elem.name)
        else:
            _log('... deleted app : ' + elem.name)


def _update_wf_websites(ctx):
    """Updates the wf websites so that they point to the correct application."""
    def _can_update(elem):
        """Predicate returning true if a stack element can be updated."""
        return elem.type == 'app' and elem.website in ctx.wf_website_list

    def _update(website, app=None):
        """Action to updates a stack element."""
        website['website_apps'] = [] if app is None else [[app, '/']]
        ctx.wf.update_website(ctx.wf_session,
                              website['name'],
                              website['ip'],
                              website['https'],
                              website['subdomains'],
                              *website['website_apps'])

    # For each app updated the associated website.
    for elem in [e for e in ctx.wf_stack if _can_update(e)]:
        msg = "... updating website {0} to point towards {1}"
        _log(msg.format(elem.website, elem.name))

        website = ctx.wf_website_list[elem.website]
        _update(website)
        _update(website, elem.name)

        msg = "... updated website {0} to point towards {1}"
        _log(msg.format(elem.website, elem.name))


def _update_repos(ctx):
    """Updates source code repositories."""
    subprocess.call([
        _EXEC,
        "stack-update-repos"
        ])


def _install_source(ctx):
    """Installs source code."""
    subprocess.call([
        _DEPLOY,
        "install_source",
        ctx.environment,
        ctx.release_id,
        ctx.api_db_pwd,
        ctx.api_port
        ])


def _restore_db(ctx):
    """Installs databases from backups."""
    subprocess.call([
        _DEPLOY,
        "restore_db",
        ctx.environment,
        ctx.release_id,
        ctx.api_db_pwd
        ])


def _restart_api(ctx):
    """Restarts API."""
    subprocess.call([
        _DEPLOY,
        "restart_api",
        ctx.environment,
        ctx.release_id
        ])


def _stop_api(ctx):
    """Stops API."""
    subprocess.call([
        _DEPLOY,
        "stop_api",
        ctx.environment,
        ctx.release_id
        ])


# Set of actions.
_actions = {
    'rollout' : [
        (_declare_stack, "Declaring stack"),
        (_set_wf_session, "Initialising web faction session"),
        (_create_wf_apps, "Creating apps upon web faction server"),
        (_create_wf_dbs, "Creating databases upon web faction server"),
        (_refresh_wf_session, "Refreshing web faction session"),
        (_set_api_port, "Assigning API port"),
        (_update_repos, "Updating repositories"),
        (_install_source, "Installing source(s)"),
        (_restore_db, "Restoring database(s)"),
        (_restart_api, "Restarting services"),
        # (_update_wf_websites, "Updating web faction websites")
    ],
    'rollback' : [
        (_declare_stack, "Declaring stack"),
        (_set_wf_session, "Initialising web faction session"),
        (_stop_api, "Stopping services"),
        (_delete_wf_apps, "Deleting apps from web faction server"),
        (_delete_wf_dbs, "Deleting databases from web faction server")
    ]
}


def _main(action, environment, version, wf_machine, wf_pwd, api_db_pwd):
    """Main entry point."""
    # Instantiate processing context.
    ctx = DeploymentContext(environment,
                            version,
                            wf_machine,
                            wf_pwd,
                            api_db_pwd)

    # Execute actions.
    for index, action_info in enumerate(_actions[action]):
        func = action_info[0]
        desc = action_info[1]
        msg = "Step {0}. {1}.".format(index, desc)
        _log(msg)
        func(ctx)


# Main entry point.
if __name__ == "__main__":
    if len(sys.argv) != 7:
        raise DeploymentError("Expecting 6 deployment arguments.")
    if sys.argv[1] not in _actions:
        raise DeploymentError("Deployment method unrecognised.")

    _main(sys.argv[1],
          sys.argv[2],
          sys.argv[3],
          sys.argv[4],
          sys.argv[5],
          sys.argv[6])
