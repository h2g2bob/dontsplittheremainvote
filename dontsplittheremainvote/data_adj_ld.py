from . import data_ge2017
from . import data_eu2019
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
        for constituency, result in data_ge2017.DATA_2017.results_by_constituency.items()
        if constituency.country != 'Northern Ireland'}

DATA_2017 = Dataset(
    code='ge2017_ld',
    title='2017 General Election results, adjusted for Lib Dem-leaning opinion polls',
    longdesc=DOC_2017,
    datafunc=_get_data_2017)


DOC_2019 = """European Parliament 2019 results, adjusted for Lib-Dem-skewed polling

Using an opinion poll which is favourable to the Liberal Democrats.
https://yougov.co.uk/topics/politics/articles-reports/2019/10/11/political-trackers-8-9-oct-update

               Con   Lab   LibDem   Brexit   Green   SNP
YouGov          35    22       22       12       5

               Con   Lab   LibDem   Brexit   Green   SNP
2019 Election    9    14       20       31      12     4
Change         +26    +8       +2      -19      -7

""" + data_eu2019.SOURCE

def _get_data_2019():
    adjustments = {
        CON: +0.26,
        LAB: +0.08,
        LD: +0.02,
        UKIP: -0.19,
        GREEN: -0.07,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_eu2019.DATA_2019.results_by_constituency.items()
        if constituency.country != 'Northern Ireland'}

DATA_2019 = Dataset(
    code='eu2019_ld',
    title='2019 European Parliament election results, adjusted for Lib Dem-leaning opinion polls',
    longdesc=DOC_2019,
    datafunc=_get_data_2019)
