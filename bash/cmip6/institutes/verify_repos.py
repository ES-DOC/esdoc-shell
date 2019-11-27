"""
.. module:: verify_repos.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Verifies that all CMIP6 instituional repos exist.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import os

from cmip6.utils import io_mgr
from cmip6.utils import vocabs



def _main():
    """Main entry point.

    """
    for i in vocabs.get_institutes():
        folder = io_mgr.get_folder([i])
        if  not os.path.exists(folder):
            print("TODO: initialise {} repo".format(i.canonical_name))


# Main entry point.
if __name__ == '__main__':
    _main()
