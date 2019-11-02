from csv import DictReader
from collections import defaultdict
from typing import Dict
from .party import get_party
from .constituency import Constituency
from .constituency import get_constitiuency
from .result import Result
from .dataset import Dataset

SOURCE = """Election results are collected as a Research Briefing by the UK Parliament, and can be downloaded from:
https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-7979

Contains Parliamentary information licensed under the Open Parliament Licence v3.0.
https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/
"""

DOC = """Results of the 2017 General Election

""" + SOURCE

def _results_by_constituency() -> Dict[Constituency, Result]:
    raw_data = defaultdict(dict)

    with open('data/ge2017/HoC-GE2017-results-by-candidate.csv', 'r') as f:
        csvf = DictReader(f)
        for row in csvf:
            constituency = row['ons_id']
            party = row['party_name']
            votes = float(row['share'])
            raw_data[constituency][party] = votes

    return {
        get_constitiuency(constituency_id): Result({
            get_party(party_name): vote_share
            for party_name, vote_share in constituency_results.items()})
        for constituency_id, constituency_results in raw_data.items()}

DATA_2017 = Dataset(
    code='ge2017',
    title='General Election 2017',
    election_result=True,
    longdesc=DOC,
    datafunc=_results_by_constituency)
