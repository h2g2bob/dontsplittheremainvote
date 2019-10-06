from . import data_eu2019
from .dataset import Dataset
from .party import CON
from .party import GREEN
from .party import LAB
from .party import LD
from .party import UKIP

DESCRIPTION_2019 = Dataset(name='eu2019_adjust_avg', description='2019 European Parliament results (estimated), adjusted for recent opinion polls')

def get_data_2019():
    """
    HoC 2015 results, adjusted to polling			
    https://ukpollingreport.co.uk/blog/archives/10089

    Election:
        BX 30.5
        LD 19.6
        L  13.7
        G  11.8
        C   8.8
        SNP 3.5
        PC  1.0

    Polling:
        L  25.2
        LD 18.0
        C  34.4
        BX 16.0
        G   4.7
    """
    adjustments = {
        LAB: 0.252 - 0.137,
        LD: 0.180 - 0.196,
        CON: 0.340 - 0.088,
        UKIP: 0.160 - 0.305,
        GREEN: 0.047 - 0.118,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_eu2019.get_data().items()}
