import os

import xlsxwriter

from cmip6.utils import logger


def init(ctx):
    """Write topic workbook.

    """
    path = os.path.join(os.getenv('ESDOC_HOME'), 'repos/institutional')
    path = os.path.join(path, ctx.institution_id)
    path = os.path.join(path, ctx.MIP_ERA)
    path = os.path.join(path, 'models')
    path = os.path.join(path, ctx.source_id)
    if not os.path.isdir(path):
        os.makedirs(path)
    fname = '_'.join([ctx.MIP_ERA, ctx.institution_id, ctx.source_id])
    fname += '_coupling.xlsx'
    path = os.path.join(path, fname)

    logger.log('generating --> {}'.format(fname), app='SH')
    ctx.wb = xlsxwriter.Workbook(path)
