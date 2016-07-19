# -*- coding: utf-8 -*-
from esdoc_api import config
from esdoc_api import db



def _main():
    """Main entry point.

    """
    # Start session.
    db.session.start(config.db)

    # Create db.
    db.session.create_repo()

    # End session.
    db.session.end()


# Main entry point.
if __name__ == '__main__':
    _main()

