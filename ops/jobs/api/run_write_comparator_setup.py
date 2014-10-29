# -*- coding: utf-8 -*-
import os, json

from tornado.options import define, options

from pyesdoc import config
from esdoc_api import db



# Define command line options.
define("outdir", help="Path to directory to which to write outputs")


# Set of project comparators for which to write setup data in json format.
_PROJECT_COMPARATORS = [
    ('CMIP5', 'c1')
    ]


def _get_c1_setup_data(project_id):
    """Loads setup data for the c1 comparator.

    """
    return {
        'fields' : db.utils.get_node_field_set(project_id),
        'nodes' : db.utils.get_node_set(project_id),
    }


# Set of supported comparator setup function pointers.
_COMPARATOR_INFO = {
    'c1' : {
        'title' : 'Model Component Properties',
        'setup' : _get_c1_setup_data
    }
}


def _get_project_id(code):
    """Returns project id.

    """
    project = db.dao.get_by_name(db.models.Project, code)
    if project is None:
        msg = 'Project code ({0}) is unsupported.'
        msg = msg.format(code)
        rt.throw(msg)

    return project.ID


def _get_setup_data(project, comparator):
    """Returns comparator setup data.

    """
    project_id = _get_project_id(project)
    title = _COMPARATOR_INFO[comparator]['title']
    data = _COMPARATOR_INFO[comparator]['setup'](project_id)

    return {
        'comparator' : comparator,
        'title' : title,
        'project' : project_id,
        'data' : data
    }


def _write_json(fpath, data):
    """Writes setup data json file.

    """
    with open(fpath, 'w') as io_stream:
        io_stream.write('esdocSetupData = ')
        json.dump(data, io_stream, encoding="ISO-8859-1")


def _write_jsonp(fpath, data):
    """Writes setup data json file.

    """
    with open(fpath + 'p', 'w') as io_stream:
        io_stream.write('onESDOC_JSONPLoad(esdocSetupData = ')
        json.dump(data, io_stream, encoding="ISO-8859-1")
        io_stream.write(');')


def _write(project, comparator):
    """Writes comparator setup data to the file system.

    """
    # Set output file path.
    fpath = "compare.setup.{0}.{1}.json".format(project.lower(), comparator)
    fpath = os.path.join(options.outdir, fpath)

    # Set setup data.
    data = _get_setup_data(project, comparator)

    # Write to file system.
    _write_json(fpath, data)
    _write_jsonp(fpath, data)


def _main():
    """Main entry point.

    """
    # Start session.
    db.session.start(config.api.db)

    # Write setup files.
    for project, comparator in _PROJECT_COMPARATORS:
        _write(project, comparator)

    # End session.
    db.session.end()



# Main entry point.
if __name__ == '__main__':
    options.parse_command_line()
    _main()

