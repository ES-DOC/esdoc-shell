"""
.. module:: convert_document.py
   :copyright: @2013 Earth System Documentation (http://es-doc.org)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Converts a document held upon local file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import sys

import pyesdoc



def _main(fpath, encoding):
    """Main entry point."""
    pyesdoc.convert_file(fpath, encoding)



# Entry point.
if __name__ == '__main__':
    _main(sys.argv[1], sys.argv[2])
