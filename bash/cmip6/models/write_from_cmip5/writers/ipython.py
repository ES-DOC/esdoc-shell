# -*- coding: utf-8 -*-

"""
.. module:: writer_ipython.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Writes mapped lightweight IPython output to file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import os
import json

import pyessv


def write(obj, output_dir):
	"""Writes mapped IPython notebook output to file system.

	:param dict obj: Mapped CMIP5 document.
	:param str output_dir: Directory to which output will be written.

	"""
	if not obj['content']:
		return

	dpath = os.path.join(output_dir, obj['institute'])
	dpath = os.path.join(dpath, obj['mipEra'])
	dpath = os.path.join(dpath, 'models')
	dpath = os.path.join(dpath, obj['sourceID'])
	fpath = os.path.join(dpath, '.{}.json'.format(obj['topic']))
	fpath = fpath.lower()

	with open(fpath, 'w') as fstream:
		fstream.write(json.dumps(obj, indent=4))
