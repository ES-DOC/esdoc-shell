import cim
import ipython


_MAPPERS = {cim, ipython}


def get_writer(encoding):
	"""Returns encoding specific writer.

	:param str encoding: Type of encoding being written.

	:returns: A writer.
	:rtype: module

	"""
	if encoding == 'cim':
		return cim
	return ipython
