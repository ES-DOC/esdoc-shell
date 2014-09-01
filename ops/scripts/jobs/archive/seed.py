"""
.. module:: seed.py
   :copyright: @2013 Earth System Documentation (http://es-doc.org)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Seeds document archive.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import sys

import pyesdoc



def _main(throttle):
    """Main entry point."""
    try:
        throttle = int(throttle)
    except ValueError:
        msg = "Archive seed throttle must be a positive integer value"
        raise ValueError(msg)

    pyesdoc.archive.seed(throttle)


# Entry point.
if __name__ == '__main__':
    _main(0 if len(sys.argv) < 2 else sys.argv[1])
