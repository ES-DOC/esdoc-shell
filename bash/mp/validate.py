# -*- coding: utf-8 -*-

"""
.. module:: validate.py
   :platform: Unix, Windows
   :synopsis: Validate an esdoc-mp schema.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import argparse
import datetime
import os

import esdoc_mp



# Define command line options.
_ARGS = argparse.ArgumentParser("Emits a validation report over an ontology schema.")
_ARGS.add_argument(
    "--ontology",
    help="The ontology to be validated.",
    dest="ontology",
    type=str
    )
_ARGS.add_argument(
    "--version",
    help="The version of the ontology to be validated.",
    dest="version",
    type=str
    )

# Report line break.
_LINE_BREAK = '\n'

# Filepath to report to be written.
_FPATH = "{}/validate_report_{}_{}.txt"

# Report section break.
_SECTION_BREAK = '------------------------------------------------------------------------------\n'



def _write_report(errors, ontology, version):
	"""Writes error report to file system.

	"""
	fpath = _FPATH.format(os.path.dirname(__file__), ontology, version)
	with open(fpath, 'w') as report:
		report.write(_SECTION_BREAK)
		report.write("ES-DOC {} {} SCHEMA VALIDATION REPORT @ {}\n".format(ontology, version, datetime.datetime.now()))
		report.write(_SECTION_BREAK)
		report.write(_LINE_BREAK)
		for error in errors:
			report.write("{}\n".format(error))

	return fpath


def _main(args):
	"""Main entry point.

	"""
	# Get schema.
	schema = esdoc_mp.get_schema(args.ontology, args.version)

	# Get errors.
	errors = esdoc_mp.validate(schema)

	# Display report.
	if errors:
		fpath = _write_report(errors, args.ontology, args.version)
		print("ES-DOC NOTEBOOK [WARNING] :: {} {} schema is invalid !!! :: {} ERROR(S)".format(args.ontology, args.version, len(errors)))
		print("ES-DOC NOTEBOOK [INFO] :: {} {} schema validation report written to {}".format(args.ontology, args.version, fpath))
	else:
		print("ES-DOC NOTEBOOK [INFO] :: {} {} schema is valid".format(args.ontology, args.version))



# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())