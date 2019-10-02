from . import data_ge2015
from .dataset import Dataset
from .party import LAB
from .party import LD
from .party import CON
from .party import UKIP

DESCRIPTION = Dataset(name='ge2015_adjust_avg', description='2015 General Election results, adjusted for recent opinion polls')

def get_data():
    """
    HoC 2015 results, adjusted to polling			
    https://ukpollingreport.co.uk/blog/archives/10089			
                
        Election	Current polling	Adjustment
    L	30.40%	25.20%	-5.20%
    LD	7.90%	18.00%	10.10%
    C	36.80%	30.40%	-6.40%
    U/B 12.6%    16.00%  3.4%
    """
    adjustments = {
        LAB: -0.052,
        LD: +0.101,
        CON: -0.064,
        UKIP: +0.034,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_ge2015.get_data().items()}
