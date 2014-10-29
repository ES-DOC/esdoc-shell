"""
.. module:: archive_organize.py
   :copyright: @2013 Earth System Documentation (http://es-doc.org)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Organizes document archive.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from tornado.options import define, options

import pyesdoc



# Define command line options.
define("organize_limit",
       default=0,
       help="Limit upon number of documents to organize (0 = unlimited)",
       type=int)



def _main():
    """Main entry point."""
    pyesdoc.archive.organize(options.organize_limit)



# Entry point.
if __name__ == '__main__':
    options.parse_command_line()
    _main()
