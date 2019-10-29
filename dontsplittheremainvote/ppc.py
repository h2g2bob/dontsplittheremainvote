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
    with open('data/democlub-candidates/candidates-parl.2019-12-12.csv', 'r') as f:
        csvf = DictReader(f)
        for row in csvf:
            candidate_name = row['name']
            candidate_link = 'https://whocanivotefor.co.uk/person/{}/'.format(row['id'])

            assert row['post_id'].startswith('WMC:')
            ons_id = row['post_id'][4:]
            constituency = get_constitiuency(ons_id)

            party = get_party(row['party_name'])

            candidates[constituency].append(PPC(
                party=party,
                name=candidate_name,
                link=candidate_link))
    assert len(candidates) > 600
    return candidates
