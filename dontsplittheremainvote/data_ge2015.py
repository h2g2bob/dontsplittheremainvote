from csv import DictReader
from collections import defaultdict
from typing import Dict
from .party import get_party
from .party import CLAIREWRIGHT
from .party import INDEPENDENT
from .constituency import Constituency
from .constituency import get_constitiuency
from .result import Result
from .dataset import Dataset

SOURCE = """Election results are collected as a Research Briefing by the UK Parliament, and can be downloaded from:
https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-7186

Contains Parliamentary information licensed under the Open Parliament Licence v3.0.
https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/"""

DOC = """Results of the 2015 General Election

""" + SOURCE

def _results_by_constituency() -> Dict[Constituency, Result]:
    raw_data = defaultdict(dict)

    with open('data/ge2015/hocl-ge2015-results-full.csv', 'r') as f:
        csvf = DictReader(f)
        for row in csvf:
            constituency = row['ons_id']
            party = get_party(row['party_name'])
            if party == INDEPENDENT and row['firstname'] == 'Claire' and row['surname'] == 'Wright':
                party = CLAIREWRIGHT
            votes = float(row['share'])
            raw_data[constituency][party] = votes

    return {
        get_constitiuency(constituency_id): Result({
            party: vote_share
            for party, vote_share in constituency_results.items()})
        for constituency_id, constituency_results in raw_data.items()}

DATA_2015 = Dataset(
    code='ge2015',
    title='General Election 2015',
    election_result=True,
    longdesc=DOC,
    datafunc=_results_by_constituency)
