from . import data_ge2017
from .dataset import Dataset
from .party import CON
from .party import GREEN
from .party import LAB
from .party import LD
from .party import SNP
from .party import UKIP

DOC_2017 = """HoC 2017 results, adjusted for Conservative-skewed polling

Using an opinion poll which is favourable to the Conseravtives:
https://www.opinium.co.uk/political-polling-25th-october-2019-2/

               Con   Lab   LibDem   Brexit   Green   SNP
Opinium         42    26       16        9       2     4

               Con   Lab   LibDem   Brexit   Green   SNP
2017 Election   42    40        7        2       1     3
Change          +0   -14       +9       +7      +1    +1

""" + data_ge2017.SOURCE

def _get_data_2017():
    adjustments = {
        CON: +0.00,
        LAB: -0.14,
        LD: +0.09,
        UKIP: +0.07,
        GREEN: +0.01,
        SNP: +0.01,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_ge2017.DATA_2017.results_by_constituency.items()
        if constituency.country != 'Northern Ireland'}

DATA_2017 = Dataset(
    code='ge2017_con',
    title='2017 General Election results, adjusted for Conservative-leaning opinion polls',
    longdesc=DOC_2017,
    datafunc=_get_data_2017)
