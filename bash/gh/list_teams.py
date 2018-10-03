# -*- coding: utf-8 -*-

"""
.. module:: init_gh_team.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initializes an ES-DOC-OPS GitHub user team.

.. moduleauthor:: Mark A. Conway-Greenslade


"""
import _utils as utils



def _main():
	"""Main entry point.

	"""
	for team in sorted(utils.get_teams()):
		print(team)


# Main entry point.
if __name__ == '__main__':
    _main()
