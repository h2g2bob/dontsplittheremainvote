from . import data_ge2017
from . import data_eu2019
from .dataset import Dataset
from .party import LAB
from .party import LD
from .party import CON
from .party import GREEN
from .party import UKIP

DOC_2017 = """HoC 2017 results, adjusted for Labour-skewed polling

Using an opinion poll which is favourable to Labour.
https://ukpollingreport.co.uk/blog/archives/10089

Opinium/Observer (9th Aug) – CON 31%, LAB 28%, LDEM 13%, BREX 16%, GRN 5% (tabs)

Election 2017: C 42.40%, L 40.00%. LD 7.40%, UKIP: 1.8%, G 1.6%

Difference: C -11.4%, L -12.0%, LD +5.6%, BX/UKIP +14.2%, G +3.4%

""" + data_ge2017.SOURCE

def _get_data_2017():
    adjustments = {
        CON: -0.114,
        LAB: -0.120,
        LD: +0.056,
        UKIP: +0.142,
        GREEN: +0.034,
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
https://ukpollingreport.co.uk/blog/archives/10089

               Con   Lab   LibDem   Brexit   Green   SNP
Opinium         31    28       13       16       5

               Con   Lab   LibDem   Brexit   Green   SNP
2019 Election    9    14       20       31      12     4
Change         +22   +14       -7      -15      -7

""" + data_eu2019.SOURCE

def _get_data_2019():
    adjustments = {
        CON: +0.22,
        LAB: +0.14,
        LD: -0.07,
        UKIP: -0.15,
        GREEN: -0.07,
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
