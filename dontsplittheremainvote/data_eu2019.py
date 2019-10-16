from csv import DictReader
from collections import defaultdict
from typing import Dict
from . import party
from .constituency import Constituency
from .constituency import get_constitiuency
from .result import Result
from .dataset import Dataset

SOURCE = """EP2019 results mapped onto Westminster constituencies by Chris Hanretty

Notes on this blog post:
https://medium.com/@chrishanretty/ep2019-results-mapped-onto-westminster-constituencies-8a2a6ed14146

The data here is an export of:
https://docs.google.com/spreadsheets/d/1G_zdsUdYjvZKOCm1F_cE4vuTI6KKXNMwMQE_z8-ZiWg/edit#gid=1595021733
"""

DOC = """Results of the 2019 European Parliament Election

""" + SOURCE

FILE = 'data/eu2019/Estimates of the EP2019 vote in Westminster constituencies - export.csv'

PARTIES = [
    (party.UKIP, 'BRX_pct'),
    (party.CON, 'CON_pct'),
    (party.GREEN, 'GRN_pct'),
    (party.LAB, 'LAB_pct'),
    (party.LD, 'LD_pct'),
    (party.PLAID, 'PC_pct'),
    (party.SNP, 'SNP_pct'),
    (party.OTHERS, 'Other_pct'),
]

def _results_by_constituency() -> Dict[Constituency, Result]:
    raw_data = defaultdict(dict)

    with open(FILE, 'r') as f:
        csvf = DictReader(f)
        for row in csvf:
            constituency = row['PCON11CD']
            for party_name, colname_pc in PARTIES:
                    party = party_name
                    votes = float(row[colname_pc])
                    raw_data[constituency][party] = votes

    return {
        get_constitiuency(constituency_id): Result({
            party: vote_share
            for party, vote_share in constituency_results.items()})
        for constituency_id, constituency_results in raw_data.items()}

DATA_2019 = Dataset(
    code='eu2019',
    title='European Parliament 2019',
    longdesc=DOC,
    datafunc=_results_by_constituency)
