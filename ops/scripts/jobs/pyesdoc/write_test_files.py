"""
.. module:: write_test_files.py
   :copyright: @2013 Earth System Documentation (http://es-doc.org)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Writes test files to the file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import sys
from os.path import join, splitext

import pyesdoc
import pyesdoc.ontologies.cim as cim
import test_utils as tu
import test_types as tt



def _get_file_path(dirpath, mod, encoding):
    """Returns test file path in readiness for io."""
    path = join(dirpath, mod.DOC_FILE)
    path = splitext(path)[0]
    path = path + "." + encoding

    return path


def _write_file(dirpath, mod, doc, encoding):
    """Writes test file to file system."""
    fpath = _get_file_path(dirpath, mod, encoding)
    with open(fpath, 'w') as op_file:
        encoded = pyesdoc.encode(doc, encoding)
        op_file.write(encoded)


def _main(dirpath):
    """Main entry point."""
    print dirpath
    return
    
    for mod in tt.MODULES:
        doc = tu.get_doc(mod)
        for encoding in pyesdoc.ESDOC_ENCODINGS_FILE:
            try:
                _write_file(dirpath, mod, doc, encoding)
            except Exception as err:
                msg = "ERR:: {0} :: {1}".format(doc.type_key, err)
                print(msg)


# Entry point.
if __name__ == '__main__':
    _main(sys.argv[1])
