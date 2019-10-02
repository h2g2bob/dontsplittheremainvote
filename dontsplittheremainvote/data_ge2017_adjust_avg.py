from . import data_ge2017
from .dataset import Dataset
from .party import LAB
from .party import LD
from .party import CON
from .party import UKIP

DESCRIPTION = Dataset(name='ge2017_adjust_avg', description='2017 General Election results, adjusted for recent opinion polls')

def get_data():
    """
    HoC 2017 results, adjusted to polling			
    https://ukpollingreport.co.uk/blog/archives/10089			

    	Election	Current polling	Adjustment
    L	40.00%	25.20%	-14.80%
    LD	7.40%	18.00%	10.60%
    C	42.40%	30.40%	-12.00%
    U/B 12.6%   16.0%   +3.4%
    """
    adjustments = {
        LAB: -0.148,
        LD: +0.106,
        CON: -0.120,
        UKIP: +0.034,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_ge2017.get_data().items()}
