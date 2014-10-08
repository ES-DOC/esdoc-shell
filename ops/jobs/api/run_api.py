# -*- coding: utf-8 -*-
import sys

from pyesdoc import db
import esdoc_api



try:
	if len(sys.argv) > 1:
		esdoc_api.run(sys.argv[1])
	else:
		esdoc_api.run()
except Exception as err:
	print err
	try:
		esdoc_api.stop()
	except:
		pass
	try:
		db.session.rollback()
	except:
		pass
finally:
	sys.exit()