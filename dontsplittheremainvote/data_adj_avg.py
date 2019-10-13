from . import data_ge2015
from . import data_ge2017
from . import data_eu2019
from .dataset import Dataset
from .party import CON
from .party import GREEN
from .party import LAB
from .party import LD
from .party import SNP
from .party import UKIP

RECENT_POLLING = """October polling:

               Con   Lab   LibDem   Brexit   Green   SNP
ComRes          33    27       19       13       3     4
Opinium         38    23       15       12       4     5
YouGov          35    22       22       12       5

https://www.comresglobal.com/polls/the-telegraph-voting-intention-october-2019/
https://www.opinium.co.uk/political-polling-3rd-october-2019/
https://yougov.co.uk/topics/politics/articles-reports/2019/10/11/political-trackers-8-9-oct-update

               Con   Lab   LibDem   Brexit   Green   SNP
October Avg     35    24       19       12       4     4
"""

DOC_2015 = """Results of the 2015 General Election, adjusted for an average opinion poll

""" + RECENT_POLLING + """
               Con   Lab   LibDem   Brexit   Green   SNP
2015 Election   37    30        8       13       4     5

               Con   Lab   LibDem   Brexit   Green   SNP
Change          -2    -6      +11       -1       0    -1

The difference numbers are added the the percentage each party got in the election,
and the results normalized to add up to 100%.

""" + data_ge2015.SOURCE

def _get_data_2015():
    adjustments = {
        CON: -0.02,
        LAB: -0.06,
        LD: +0.11,
        UKIP: -0.01,
        SNP: -0.01,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_ge2015.DATA_2015.results_by_constituency.items()}

DATA_2015 = Dataset(
    code='ge2015_avg',
    title='2015 General Election results, adjusted for recent opinion polls',
    longdesc=DOC_2015,
    datafunc=_get_data_2015)


DOC_2017 = """Results of the 2017 General Election, adjusted for an average opinion poll

""" + RECENT_POLLING + """
               Con   Lab   LibDem   Brexit   Green   SNP
2017 Election   42    40        7        2       1     3

               Con   Lab   LibDem   Brexit   Green   SNP
Change          -7   -16      +12      +10      +3    +1

The difference numbers are added the the percentage each party got in the election,
and the results normalized to add up to 100%.

""" + data_ge2017.SOURCE

def _get_data_2017():
    adjustments = {
        CON: -0.07,
        LAB: -0.16,
        LD: +0.12,
        UKIP: +0.10,
        GREEN: +0.03,
        SNP: +0.01,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_ge2017.DATA_2017.results_by_constituency.items()}

DATA_2017 = Dataset(
    code='ge2017_avg',
    title='2017 General Election results, adjusted for recent opinion polls',
    longdesc=DOC_2017,
    datafunc=_get_data_2017)


DOC_2019 = """Results of the 2019 European Parliament Election, adjusted for an average opinion poll

""" + RECENT_POLLING + """
               Con   Lab   LibDem   Brexit   Green   SNP
2019 Election    9    14       20       31      12     4

               Con   Lab   LibDem   Brexit   Green   SNP
Change         +26   +10       -1      -19      -6     0

The difference numbers are added the the percentage each party got in the election,
and the results normalized to add up to 100%.

""" + data_eu2019.SOURCE

def _get_data_2019():
    adjustments = {
        CON: +0.26,
        LAB: +0.10,
        LD: -0.01,
        UKIP: -0.19,
        GREEN: -0.06,
        SNP: +0.00,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_eu2019.DATA_2019.results_by_constituency.items()}

DATA_2019 = Dataset(
    code='eu2019_avg',
    title='2019 European Parliament results (estimated), adjusted for recent opinion polls',
    longdesc=DOC_2019,
    datafunc=_get_data_2019)
