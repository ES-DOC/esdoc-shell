# -*- coding: utf-8 -*-
import sys

import esdoc_api




def _main():
    """Main entry point.

    """
    try:
        esdoc_api.run()
    except Exception as err:
        print err
        try:
            esdoc_api.stop()
        except:
            pass
        try:
            esdoc_api.db.session.rollback()
        except:
            pass
    finally:
        sys.exit()


# Main entry point.
if __name__ == '__main__':
    _main()