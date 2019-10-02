from . import data_ge2017
from .dataset import Dataset
from .party import LAB
from .party import LD
from .party import CON
from .party import GREEN
from .party import UKIP

DESCRIPTION_2017 = Dataset(name='ge2017_adjust_lab', description='2017 General Election results, adjusted for labour-leaning polls')

def get_data_2017():
    """
    HoC 2017 results, adjusted for conservative-skewed polling
    https://ukpollingreport.co.uk/blog/archives/10089

    Opinium/Observer (9th Aug) – CON 31%, LAB 28%, LDEM 13%, BREX 16%, GRN 5% (tabs)

    Election 2017: C 42.40%, L 40.00%. LD 7.40%, UKIP: 1.8%, G 1.6%

    Difference: C -11.4%, L -12.0%, LD +5.6%, BX/UKIP +14.2%, G +3.4%
    """
    adjustments = {
        CON: -0.114,
        LAB: -0.120,
        LD: +0.056,
        UKIP: +0.142,
        GREEN: +0.034,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_ge2017.get_data().items()}
