import cim
import ipython


_MAPPERS = {cim, ipython}


def get_mapper(encoding):
	"""Returns encding specific mapper.

	:param str encoding: Type of encoding to be mapped.

	:returns: A mapper.
	:rtype: module

	"""
	if encoding == 'cim':
		return cim
	return ipython
