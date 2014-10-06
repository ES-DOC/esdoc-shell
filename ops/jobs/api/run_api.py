# -*- coding: utf-8 -*-
import sys

import esdoc_api


if len(sys.argv) > 1:
	esdoc_api.run(sys.argv[1])
else:
	esdoc_api.run()
