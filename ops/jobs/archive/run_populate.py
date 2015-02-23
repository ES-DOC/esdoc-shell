# -*- coding: utf-8 -*-

"""
.. module:: populate.py
   :copyright: @2013 Earth System Documentation (http://es-doc.org)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Populates archive with documents pulled from remote sources.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from tornado.options import define, options

import pyesdoc


# Define command line options.
define("populate_limit",
       default=0,
       help="Limit upon number of documents to import (0 = unlimited)",
       type=int)


def _main():
    """Main entry point.

    """
    pyesdoc.archive.populate(options.populate_limit)



# Entry point.
if __name__ == '__main__':
    options.parse_command_line()
    _main()
