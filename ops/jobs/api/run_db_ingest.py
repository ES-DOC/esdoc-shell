# -*- coding: utf-8 -*-
from tornado.options import define, options

from esdoc_api import db, config



# Define command line options.
define("throttle", help="Limit upon number of documents to ingest", type=int, default=0)


def _main():
    """Main entry point.

    """
    # Start session.
    db.session.start(config.db)

    # Ingest documents into db.
    db.ingest.execute(options.throttle)

    # End session.
    db.session.end()



# Main entry point.
if __name__ == '__main__':
    options.parse_command_line()
    _main()
