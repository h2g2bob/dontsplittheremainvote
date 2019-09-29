from . import data_ge2017
from .dataset import Dataset
from .party import LAB
from .party import LD
from .party import CON
from .party import GREEN
from .party import UKIP

DESCRIPTION_2017 = Dataset(name='ge2017_adjust_bx', description='2017 General Election results, adjusted for Brexit Party-leaning polls')

def get_data_2017():
    """
    HoC 2017 results, adjusted for brexit-skewed polling
    https://ukpollingreport.co.uk/blog/archives/10083

    Opinium: CON 23%, LAB 25%, LDEM 15%, BREX 22%, GRN 8%

    Election 2017: C 42.40%, L 40.00%. LD 7.40%, UKIP 1.8%, G 1.6%

    Difference: C -19.4%, L -15.0%, LD +7.6%, BX/UKIP +20.2%, G +6.4%
    """
    adjustments = {
        CON: -0.194,
        LAB: -0.150,
        LD: +0.076,
        UKIP: +0.202,
        GREEN: +0.064,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_ge2017.get_data().items()}
