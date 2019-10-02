from . import data_ge2017
from .dataset import Dataset
from .party import LAB
from .party import LD
from .party import CON
from .party import GREEN
from .party import UKIP

DESCRIPTION_2017 = Dataset(name='ge2017_adjust_ld', description='2017 General Election results, adjusted for lib-dem-leaning polls')

def get_data_2017():
    """
    HoC 2017 results, adjusted for conservative-skewed polling
    https://ukpollingreport.co.uk/blog/archives/10092

    YouGov: CON 33%, LAB 22%, LDEM 21%, BREX 12%, GRN 7%

    Election 2017: C 42.40%, L 40.00%. LD 7.40%, UKIP 1.8%, G 1.6%

    Difference: C -9.4%, L -18.0%, LD +13.6%, BX/UKIP +10.2%, G +5.4%
    """
    adjustments = {
        CON: -0.094,
        LAB: -0.180,
        LD: +0.136,
        UKIP: +0.102,
        GREEN: +0.054,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_ge2017.get_data().items()}
