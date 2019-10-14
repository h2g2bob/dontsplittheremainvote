import json
from collections import defaultdict
from typing import NamedTuple
from typing import List
from typing import Dict
from .constituency import Constituency
from .constituency import get_constitiuency
from .party import Party
from .party import get_party

class OtherSiteSuggestion(NamedTuple):
    who_suggests: str
    party: Party
    url: str


def _tacticalvote():
    with open('data/tacticalvote/recommendations.json') as f:
        data = json.load(f)
        for recomend in data:
            if recomend['VoteFor'] != 'TBC':
                suggestion = OtherSiteSuggestion(
                    who_suggests='tacticalvote.co.uk',
                    party=get_party(recomend['VoteFor']),
                    url='https://tacticalvote.co.uk/#{}'.format(recomend['Constituency'].replace(' ', '')))
                yield get_constitiuency(recomend['id']), suggestion

def get_other_site_suggestions() -> Dict[Constituency, List[OtherSiteSuggestion]]:
    out = defaultdict(list)
    for constituency, suggest in _tacticalvote():
        out[constituency].append(suggest)
    return dict(out)
