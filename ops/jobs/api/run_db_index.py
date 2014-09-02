# -*- coding: utf-8 -*-
from pyesdoc import config, db



def _main():
    """Main entry point."""
    # Start session.
    db.session.start(config.api.db)

    # Index document facets.
    db.index.execute()

    # End session.
    db.session.end()


# Main entry point.
if __name__ == '__main__':
    _main()
