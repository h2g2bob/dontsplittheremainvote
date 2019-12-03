from . import data_ge2017
from . import data_eu2019
from .dataset import Dataset
from .party import CON
from .party import GREEN
from .party import LAB
from .party import LD
from .party import SNP
from .party import UKIP

DOC_2017 = """HoC 2017 results, adjusted for Labour-skewed polling

Using an opinion poll which is favourable to Labour.

https://www.comresglobal.com/polls/remain-united-election-poll-november-2019/

               Con   Lab   LibDem   Brexit   Green   SNP
2017 Election   42    40        7        2       1     3

               Con   Lab   LibDem   Brexit   Green   SNP
ComRes          43    35       11        5       2     4

               Con   Lab   LibDem   Brexit   Green   SNP
Change          +1    -5       +4       +3      +1    +1

""" + data_ge2017.SOURCE

def _get_data_2017():
    adjustments = {
        CON: +0.01,
        LAB: -0.05,
        LD: +0.04,
        UKIP: +0.03,
        GREEN: +0.01,
        SNP: +0.01,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_ge2017.DATA_2017.results_by_constituency.items()
        if constituency.country != 'Northern Ireland'}

DATA_2017 = Dataset(
    code='ge2017_lab',
    title='2017 General Election results, adjusted for Labour-leaning opinion polls',
    longdesc=DOC_2017,
    datafunc=_get_data_2017)


DOC_2019 = """European Parliament 2019 results, adjusted for Labour-skewed polling

Using an opinion poll which is favourable to Labour.
https://www.comresglobal.com/polls/remain-united-election-poll-november-2019/

               Con   Lab   LibDem   Brexit   Green   SNP
ComRes          43    35       11        5       2     4

               Con   Lab   LibDem   Brexit   Green   SNP
2019 Election    9    14       20       31      12     4
Change         +34   +21       -9      -26     -10    +0

""" + data_eu2019.SOURCE

def _get_data_2019():
    adjustments = {
        CON: +0.34,
        LAB: +0.21,
        LD: -0.09,
        UKIP: -0.26,
        GREEN: -0.10,
        SNP: +0.00,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_eu2019.DATA_2019.results_by_constituency.items()
        if constituency.country != 'Northern Ireland'}

DATA_2019 = Dataset(
    code='eu2019_lab',
    title='2019 European Parliament election results, adjusted for Labour-leaning opinion polls',
    europarl=True,
    longdesc=DOC_2019,
    datafunc=_get_data_2019)
