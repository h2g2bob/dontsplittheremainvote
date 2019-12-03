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

RECENT_POLLING = """\
Late October polling:

Oct/Nov polling:

               Con   Lab   LibDem   Brexit   Green   SNP
ComRes          36    28       17       10       3     4
Opinium         42    26       16        9       2     4
YouGov          36    21       18       13       6     4

https://www.comresglobal.com/polls/sunday-express-ge2019-voting-intention-poll/
https://www.opinium.co.uk/political-polling-25th-october-2019-2/
https://yougov.co.uk/topics/politics/articles-reports/2019/10/31/political-trackers-29-30-oct-update

Early Nov polling:

               Con   Lab   LibDem   Brexit   Green   SNP
ComRes          37    29       17        9       3     4
Opinium         41    29       15        6       2     5
YouGov          42    28       15        4       4     3

https://www.comresglobal.com/polls/britain-elects-ge2019-voting-intention-poll/
https://www.opinium.co.uk/political-polling-6th-november-2019/
https://yougov.co.uk/topics/politics/articles-reports/2019/11/12/political-trackers-11-12-nov-update

               Con   Lab   LibDem   Brexit   Green   SNP
November Avg    39    27       16        9       3     4
"""

DOC_2015 = """Results of the 2015 General Election, adjusted for an average opinion poll

""" + RECENT_POLLING + """
               Con   Lab   LibDem   Brexit   Green   SNP
2015 Election   37    30        8       13       4     5

               Con   Lab   LibDem   Brexit   Green   SNP
Change          +2    -3       +8       -4      -1    -1

The difference numbers are added the the percentage each party got in the election,
and the results normalized to add up to 100%.

""" + data_ge2015.SOURCE

def _get_data_2015():
    adjustments = {
        CON: +0.02,
        LAB: -0.03,
        LD: +0.08,
        UKIP: -0.04,
        GREEN: -0.01,
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
Change          -3   -13       +9       +7      +2    +1

The difference numbers are added the the percentage each party got in the election,
and the results normalized to add up to 100%.

""" + data_ge2017.SOURCE

def _get_data_2017():
    adjustments = {
        CON: -0.03,
        LAB: -0.13,
        LD: +0.09,
        UKIP: +0.07,
        GREEN: +0.02,
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
Change         +30   +13       -4      -22      -9     0

The difference numbers are added the the percentage each party got in the election,
and the results normalized to add up to 100%.

""" + data_eu2019.SOURCE

def _get_data_2019():
    adjustments = {
        CON: +0.30,
        LAB: +0.13,
        LD: -0.04,
        UKIP: -0.22,
        GREEN: -0.09,
        SNP: +0.00,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_eu2019.DATA_2019.results_by_constituency.items()}

DATA_2019 = Dataset(
    code='eu2019_avg',
    title='2019 European Parliament results, adjusted for recent opinion polls',
    europarl=True,
    longdesc=DOC_2019,
    datafunc=_get_data_2019)
