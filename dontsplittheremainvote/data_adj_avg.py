from . import data_ge2015
from . import data_ge2017
from . import data_eu2019
from .dataset import Dataset
from .party import CON
from .party import GREEN
from .party import LAB
from .party import LD
from .party import UKIP

DESCRIPTION_2015 = Dataset(name='ge2015_adjust_avg', description='2015 General Election results, adjusted for recent opinion polls')

def get_data_2015():
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


DESCRIPTION_2017 = Dataset(name='ge2017_adjust_avg', description='2017 General Election results, adjusted for recent opinion polls')

def get_data_2017():
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
