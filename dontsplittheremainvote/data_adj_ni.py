from . import data_ge2017
from .dataset import Dataset
from .party import ALLIANCE
from .party import DUP
from .party import GREEN
from .party import SDLP
from .party import SF
from .party import UUP

DOC_2017 = """HoC 2017 results, adjusted for Northern Ireland polling

Using the LucidTalk August 2019 opinion poll, which is focused
on Northern Ireland:
https://www.electoralcalculus.co.uk/polls_ni.html

               DUP    SF   SDLP   UUP   Al'nce   Green
LucidTalk       29    25      8     9       21       1

               DUP    SF   SDLP   UUP   Al'nce   Green
2017 Election   36    29     12    10        8       1
Change          -7    -4     -4    -1      +13      +0

""" + data_ge2017.SOURCE

def _get_data_2017():
    adjustments = {
        DUP: -0.07,
        SF: -0.04,
        SDLP: -0.04,
        UUP: -0.01,
        ALLIANCE: +0.13,
        GREEN: +0.00,
    }
    return {
        constituency: result.adjust_for_polling(adjustments)
        for constituency, result in data_ge2017.DATA_2017.results_by_constituency.items()
        if constituency.country == 'Northern Ireland'}

DATA_2017 = Dataset(
    code='ge2017_ni',
    title='2017 General Election results, adjusted for Northern Ireland polling',
    longdesc=DOC_2017,
    datafunc=_get_data_2017)
