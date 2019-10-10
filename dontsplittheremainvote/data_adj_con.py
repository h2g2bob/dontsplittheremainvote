from . import data_ge2017
from .dataset import Dataset
from .party import LAB
from .party import LD
from .party import CON
from .party import GREEN
from .party import UKIP

DOC_2017 = """HoC 2017 results, adjusted for Conservative-skewed polling

Using an opinion poll which is favourable to the Conseravtives.
https://ukpollingreport.co.uk/blog/archives/10089

Opinium: CON 37%, LAB 25%, LDEM 16%, BREX 13%, GRN 2%

Election 2017: C 42.40%, L 40.00%. LD 7.40%, UKIP 1.8%, G 1.6%

Difference: C -5.4%, L -15%, LD +8.6%, BX/UKIP +11.2%, G +0.4%

""" + data_ge2017.SOURCE

def _get_data_2017():
    adjustments = {
        CON: -0.054,
        LAB: -0.150,
        LD: +0.086,
        UKIP: +0.112,
        GREEN: +0.004,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_ge2017.DATA_2017.results_by_constituency.items()}

DATA_2017 = Dataset(
    code='ge2017_con',
    title='2017 General Election results, adjusted for Conservative-leaning opinion polls',
    longdesc=DOC_2017,
    datafunc=_get_data_2017)
