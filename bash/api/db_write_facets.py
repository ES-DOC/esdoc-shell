# -*- coding: utf-8 -*-
import csv, json, os

from tornado.options import define, options

from pyesdoc.extensions.cim.v1.software_model_component_type_map import ESDOC_METAFOR_MODEL_COMPONENT_MAP
from esdoc_api import db, config
from esdoc_api.utils import rt


# Set command line options.
define("output_dir", help="Output directory", type=str)



def _get_nodeset():
    """Returns nodes from db.

    """
    # Load from db.
    db.session.start(config.db)
    try:
        nodeset = { i.id: i for i in db.dao.get_all(db.models.Node) }
        valueset = { i.id: i for i in db.dao.get_all(db.models.NodeField) }
    finally:
        db.session.end()

    # Build intra-node references.
    for node in nodeset.values():
        node.fields = [nodeset[int(f[1:])] if f.startswith('n') else valueset[int(f)]
                       for f in node.field.split(",")]
        node.field_text = "-".join(f.text for f in node.fields if isinstance(f, db.models.NodeField))

    return nodeset


def _get_nodeset_by_type(nodeset, type_of):
    """Returns a filtered nodeset.

    """
    return sorted([n for n in nodeset.values() if n.type_of == type_of],
                  key=lambda n :n.field_text)


def _dump(nodeset, node_type, cols, row_factory, row_predicate=None):
    """Writes a nodeset dump to file system.

    """
    # Set nodeset.
    nodeset = _get_nodeset_by_type(nodeset, node_type)
    if row_predicate:
        nodeset = [n for n in nodeset if row_predicate(n)]
    rows = [row_factory(n) for n in nodeset]

    # Dump csv file.
    fpath = os.path.join(options.output_dir, 'cv-dump-{}.csv'.format(node_type).lower())
    rt.log_db("dumping {0} --> {1}".format(node_type, fpath))
    with open(fpath, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cols)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    # Dump json file.
    fpath = os.path.join(options.output_dir, 'cv-dump-{}.json'.format(node_type).lower())
    rt.log_db("dumping {0} --> {1}".format(node_type, fpath))
    with open(fpath, 'w') as jsonfile:
        jsonfile.write(json.dumps(rows, indent=4))


def _dump_institutes(nodeset):
    """Dumps set of institutes to file system.

    """
    node_type = 'Institute'
    cols = ['institute']
    row_factory = lambda node: {
        'institute': node.field_text
        }
    row_predicate = lambda node: node.field_text != '--'
    _dump(nodeset, node_type, cols, row_factory, row_predicate)


def _dump_experiments(nodeset):
    """Dumps set of experiments to file system.

    """
    node_type = 'Experiment'
    cols = ['experiment']
    row_factory = lambda node: {
        'experiment': node.field_text
        }
    _dump(nodeset, node_type, cols, row_factory)


def _dump_models(nodeset):
    """Dumps set of models to file system.

    """
    node_type = 'Model'
    cols = ['institute', 'model', 'key']
    row_factory = lambda node: {
        'institute': node.fields[0].text,
        'model': node.fields[1].text,
        'key': node.field_text
        }
    _dump(nodeset, node_type, cols, row_factory)


def _dump_model_components(nodeset):
    """Dumps set of model components to file system.

    """
    node_type = 'ModelComponent'
    cols = ['component', 'metafor component']
    row_factory = lambda node: {
        'component': node.field_text,
        'metafor component':  ESDOC_METAFOR_MODEL_COMPONENT_MAP[node.field_text]
        }
    _dump(nodeset, node_type, cols, row_factory)


def _dump_model_component_properties(nodeset):
    """Dumps set of model component properties to file system.

    """
    node_type = 'ModelComponentProperty'
    cols = ['component', 'property', 'key', 'metafor component']
    row_factory = lambda node: {
        'component': node.field_text.split(">>")[0].strip(),
        'property': node.field_text.split(">>")[1].strip(),
        'key': node.field_text,
        'metafor component': ESDOC_METAFOR_MODEL_COMPONENT_MAP[node.field_text.split(">>")[0].strip()]
        }
    _dump(nodeset, node_type, cols, row_factory)


def _dump_model_component_property_values(nodeset):
    """Dumps set of model component property values to file system.

    """
    node_type = 'ModelComponentPropertyValue'
    cols = ['institute', 'model', 'component', 'property', 'value']
    row_factory = lambda node: {
        'institute': node.fields[0].fields[0].text,
        'model': node.fields[0].fields[1].text,
        'component': node.fields[2].field_text.split(">>")[0].strip(),
        'property': node.fields[2].field_text.split(">>")[1].strip(),
        'value': node.field_text.encode('utf-8')
        }
    _dump(nodeset, node_type, cols, row_factory)


def _main():
    """Main entry point.

    """
    nodeset = _get_nodeset()
    for func in (
        _dump_institutes,
        _dump_experiments,
        _dump_models,
        _dump_model_components,
        _dump_model_component_properties,
        _dump_model_component_property_values
        ):
        func(nodeset)


# Main entry point.
if __name__ == '__main__':
    options.parse_command_line()
    _main()
