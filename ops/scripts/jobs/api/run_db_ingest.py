# -*- coding: utf-8 -*-
import sys

from pyesdoc import config, db



def _main(throttle, type_filter):
    """Main entry point."""
    # Start session.
    db.session.start(config.api.db)

    # Ingest documents into db.
    db.ingest.execute(throttle, type_filter)

    # End session.
    db.session.end()


# Main entry point.
if __name__ == '__main__':
    # Unpack throttle.
    try:
        throttle = int(sys.argv[1])
    except IndexError:
        throttle = 0
    except ValueError:
        raise ValueError("Throttle parameter must be a positive integer value")

    # Unpack type filter.
    try:
        type_filter = sys.argv[2]
    except IndexError:
        type_filter = None

    _main(throttle, type_filter)
