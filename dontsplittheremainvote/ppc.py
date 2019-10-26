from csv import DictReader
from collections import defaultdict
from .constituency import get_constitiuency
from .party import get_party
from .party import Party
from typing import NamedTuple


class PPC(NamedTuple):
    party: Party
    name: str
    link: str


def candidate_data():
    candidates = defaultdict(list)
    with open('data/democlub-early-candidates/DemoClub_PPC.csv', 'r') as f:
        csvf = DictReader(f)
        for row in csvf:
            candidate_name = row['Candidate Name']
            candidate_link = row['Existing Candidate Profile URL']
            if not candidate_name:
                continue
            ons_id = row[''] # row[11]
            constituency = get_constitiuency(ons_id)
            party = get_party(row['Party Name'])
            candidates[constituency].append(PPC(
                party=party,
                name=candidate_name,
                link=candidate_link))
    return candidates
