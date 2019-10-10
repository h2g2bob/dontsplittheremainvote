from . import data_ge2015
from . import data_ge2017
from . import data_eu2019
from .dataset import Dataset
from .party import CON
from .party import GREEN
from .party import LAB
from .party import LD
from .party import UKIP

DOC_2015 = """Results of the 2015 General Election, adjusted for an average opinion poll

Using the average of the opinion polls listed here:
https://ukpollingreport.co.uk/blog/archives/10089			

       Election   Polling   Difference
LAB       30.4%     25.2%        -5.2%
LD         7.9%     18.0%        10.1%
CON       36.8%     30.4%        -6.4%
BXT       12.6%     16.0%         3.4%

The difference numbers are added the the percentage each party got in the election,
and the results normalized to add up to 100%.

""" + data_ge2015.SOURCE

def _get_data_2015():
    adjustments = {
        LAB: -0.052,
        LD: +0.101,
        CON: -0.064,
        UKIP: +0.034,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_ge2015.DATA_2015.results_by_constituency.items()}

DATA_2015 = Dataset(
    code='ge2015_avg',
    title='2015 General Election results, adjusted for recent opinion polls',
    longdesc=DOC_2015,
    datafunc=_get_data_2015)


DOC_2017 = """Results of the 2017 General Election, adjusted for an average opinion poll

Using the average of the opinion polls listed here:
https://ukpollingreport.co.uk/blog/archives/10089			

       Election   Polling   Difference
LAB       40.0%     25.2%       -14.8%
LD         7.4%     18.0%        10.6%
CON       42.4%     30.4%       -12.0%
BXT       12.6%     16.0%         3.4%

The difference numbers are added the the percentage each party got in the election,
and the results normalized to add up to 100%.

""" + data_ge2017.SOURCE
def _get_data_2017():
    adjustments = {
        LAB: -0.148,
        LD: +0.106,
        CON: -0.120,
        UKIP: +0.034,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_ge2017.DATA_2017.results_by_constituency.items()}

DATA_2017 = Dataset(
    code='ge2017_avg',
    title='2017 General Election results, adjusted for recent opinion polls',
    longdesc=DOC_2017,
    datafunc=_get_data_2017)


DOC_2019 = """HoC 2015 results, adjusted to polling			

Using the average of the opinion polls listed here:
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

The difference numbers are added the the percentage each party got in the election,
and the results normalized to add up to 100%.

""" + data_eu2019.SOURCE

def _get_data_2019():
    adjustments = {
        LAB: 0.252 - 0.137,
        LD: 0.180 - 0.196,
        CON: 0.340 - 0.088,
        UKIP: 0.160 - 0.305,
        GREEN: 0.047 - 0.118,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_eu2019.DATA_2019.results_by_constituency.items()}

DATA_2019 = Dataset(
    code='eu2019_avg',
    title='2019 European Parliament results (estimated), adjusted for recent opinion polls',
    longdesc=DOC_2019,
    datafunc=_get_data_2019)
