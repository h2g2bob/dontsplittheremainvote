from . import data_ge2017
from .dataset import Dataset
from .party import LAB
from .party import LD
from .party import CON
from .party import GREEN
from .party import UKIP

DOC_2017 = """HoC 2017 results, adjusted for Lib-Dem-skewed polling

Using an opinion poll which is favourable to the Liberal Democrats.
https://yougov.co.uk/topics/politics/articles-reports/2019/10/11/political-trackers-8-9-oct-update

               Con   Lab   LibDem   Brexit   Green   SNP
YouGov          35    22       22       12       5

               Con   Lab   LibDem   Brexit   Green   SNP
2017 Election   42    40        7        2       1     3
Change          -7   -18      +15      +10      +4

""" + data_ge2017.SOURCE

def _get_data_2017():
    adjustments = {
        CON: -0.07,
        LAB: -0.18,
        LD: +0.15,
        UKIP: +0.10,
        GREEN: +0.04,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_ge2017.DATA_2017.results_by_constituency.items()}

DATA_2017 = Dataset(
    code='ge2017_ld',
    title='2017 General Election results, adjusted for Lib Dem-leaning opinion polls',
    longdesc=DOC_2017,
    datafunc=_get_data_2017)
