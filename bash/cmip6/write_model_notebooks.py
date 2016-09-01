# -*- coding: utf-8 -*-

"""
.. module:: write_model_notebooks.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Writes CMIP6 IPython model notebooks to file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import datetime as dt
import json
import os

from tornado.template import Template

import pyesdoc
from pyesdoc.specializations.cmip6.loader import get_specializations
from pyesdoc.specializations.cmip6.model import Realm



# Command line options.
_ARGS = argparse.ArgumentParser("Writes CMIP6 IPython model notebooks to file system.")
_ARGS.add_argument(
    "--input",
    help="Path to a directory where specializations are found.",
    dest="input_dir",
    type=str
    )
_ARGS.add_argument(
    "--output",
    help="Path to a directory into which notebooks will be written.",
    dest="output_dir",
    type=str
    )
_ARGS.add_argument(
    "--cfg",
    help="Path to a confguration file driving which notebooks will be written.",
    dest="cfg_fpath",
    type=str,
    default="{}.conf".format(__file__.split(".")[0])
    )


# The mip-era for which notebooks are to be generated.
_MIP_ERA = 'cmip6'

# Map of realm names to loaded tornado templates.
_REALM_TEMPLATES = {}


def _get_config(fpath):
    """Returns associated configuration file converted to a dictionary.

    """
    with open(fpath, 'r') as fstream:
        return json.loads(fstream.read())


def _get_specializations(input_dir, realm):
    """Returns realm specializations as a collection of python modules.

    """
    spec_dir = os.path.join(input_dir, "cmip6-specializations-{}".format(realm))
    if not os.path.isdir(spec_dir):
        raise ValueError("Specializations directory does not exist")

    return get_specializations(spec_dir, realm)


def _get_property_value(prp, output):
    """Returns either a property's default value or it's previously saved value.

    """
    if prp.short_id(2) not in output:
        return ''
    else:
        return output[prp.short_id(2)]


def _get_property_hint(prp):
    """Returns a user hint regarding how to complete a property.

    """
    def _get_property_optionality():
        """Returns a property's optional status declaration.

        """
        return "MANDATORY" if prp.is_mandatory else "OPTIONAL"


    def _get_property_cardinality():
        """Returns a property's cardinality declaration.

        """
        if prp.typeof not in ('bool', 'enum'):
            return "ARRAY" if prp.is_collection else ""

        output = "- choose {} from:"

        return output.format("MANY") if prp.is_collection else output.format("ONE")


    def _get_property_type():
        """Returns a property's type declaration.

        """
        return prp.typeof_label


    return "{} {} {}".format(
        _get_property_optionality(),
        _get_property_type(),
        _get_property_cardinality()
        )


def _get_content(realm, institute, model, output):
    """Returns notebook content.

    """
    # JIT load template.
    if realm not in _REALM_TEMPLATES:
        fpath = "{}.tornado".format(__file__.split(".")[0])
        with open(fpath, 'r') as fstream:
            _REALM_TEMPLATES[realm] = Template(fstream.read())

    # Generate notebook content.
    content = _REALM_TEMPLATES[realm].generate(
        DOC=output,
        val=_get_property_value,
        p_hint=_get_property_hint,
        mip_era=_MIP_ERA,
        institute=institute,
        model=model,
        r=realm,
        escape=lambda s: s.strip().replace('"', "'"),
        now=dt.datetime.now()
        )

    # Tidy up tornado escaping.
    return content.replace("#\n", "") \
                  .replace("#\t\n", "") \
                  .replace("#\t\t\n", "") \
                  .replace("#\t\t\t\n", "") \
                  .replace("#\t\t\t\t\n", "")


def _get_output(output_dir, institute, model, realm):
    """Reads notebook output from file system.

    """
    fpath = os.path.join(output_dir, institute)
    fpath = os.path.join(fpath, model)
    fpath = os.path.join(fpath, "{}.json".format(realm))
    if os.path.isfile(fpath):
        with open(fpath, 'r') as fstream:
            return json.loads(fstream.read())

    # If the notebook has not been run before then simply return default.
    return {
        "INSTITUTE": institute,
        "MIP_ERA": _MIP_ERA,
        "MODEL": model,
        "REALM": realm,
        "AUTHORS": "",
        "CONTRIBUTORS": ""
    }


def _write(output_dir, institute, model, realm, content):
    """Writes notebook content to file system.

    """
    fpath = os.path.join(output_dir, institute)
    fpath = os.path.join(fpath, model)
    fpath = os.path.join(fpath, "{}.ipynb".format(realm))
    with open(fpath, 'w') as fstream:
        fstream.write(content)


def _main(args):
    """Main entry point.

    """
    # Validate inputs.
    if not os.path.isdir(args.input_dir):
        raise ValueError("Specializations root folder does not exist")
    if not os.path.isdir(args.output_dir):
        raise ValueError("Output directory does not exist")
    if not os.path.isfile(args.cfg_fpath):
        raise ValueError("Configration file does not exist")

    # Load configuration file.
    cfg = _get_config(args.cfg_fpath)

    # Emit a notebook per instiute / model / realm conbination.
    for institute, model in [(i.split(":")[0], i.split(":")[1]) for i in cfg['models']]:
        for realm_name in cfg['realms']:
            # ... instantiate realm specializations wrapper;
            realm = Realm(_get_specializations(args.input_dir, realm_name))

            # ... load previously saved notebook output;
            output = _get_output(args.output_dir, institute, model, realm_name)

            # ... generate notebook content;
            content = _get_content(realm, institute, model, output)

            # ... write notebook content.
            _write(args.output_dir, institute, model, realm_name, content)


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
