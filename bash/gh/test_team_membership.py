# -*- coding: utf-8 -*-

"""
.. module:: test_team_membership.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Tests membership of a ES-DOC-OPS GitHub user team.

.. moduleauthor:: Mark A. Conway-Greenslade


"""
import argparse

import pyesdoc



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Tests membership of a ES-DOC-OPS GitHub user team.")
_ARGS.add_argument(
    "--user",
    help="A GitHub user account",
    dest="user",
    type=str
    )
_ARGS.add_argument(
    "--team",
    help="The GitHub team that the user wishes to have access to",
    dest="team",
    type=str
    )


def _main(args):
    """Main entry point.

    """
    team_id = args.team.strip().lower()
    user_id = args.user.strip()
    if not pyesdoc.security.is_team_member(team_id, user_id):
        raise ValueError('{} is not a member of {}'.format(args.user, args.team))

    pyesdoc.log('team membership confirmed')


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
