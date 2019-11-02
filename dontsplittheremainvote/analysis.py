from collections import defaultdict
from typing import List
from typing import Dict
from typing import NamedTuple
from typing import Tuple
import operator

from .classify import ClassifyResult
from .party import get_party
from .party import LAB
from .party import LD
from .party import CHANGEUK
from .party import INDEPENDENT
from .party import Party
from .result import Result

class Analysis(NamedTuple):
    template: str = 'constituency.html'
    we_recommend_party: Party = None

    def as_json(self):
        return {
            'template': self.template,
            'we_recommend_party': self.we_recommend_party.short if self.we_recommend_party is not None else None,
        }


def group_by_frequency(results: List[Result]) -> Dict[ClassifyResult, float]:
    classify_frequency = defaultdict(float)
    for result in results:
        classify_frequency[result.classify] += (1.0 / len(results))
    return dict(classify_frequency)

def outcome_frequency(results: List[Result]) -> List[Tuple[ClassifyResult, float]]:
    classify_frequency = list(group_by_frequency(results).items())
    classify_frequency.sort(key=operator.itemgetter(1), reverse=True)
    return classify_frequency

def get_analysis(results, constituency) -> Analysis:
    if constituency.slug == 'don-valley':
        return Analysis(
            template='special-labour-leave.html',
            we_recommend_party=LD)

    advice = _get_analysis(results)

    INDEPENDENT_REMAIN = {
        'broxtowe': CHANGEUK,
        'beaconsfield': INDEPENDENT,
        'eddisbury': INDEPENDENT,
        'runnymede-and-weybridge': INDEPENDENT,
        'south-west-hertfordshire': INDEPENDENT,
    }
    if constituency.slug in INDEPENDENT_REMAIN:
        return Analysis(
            template='special-independent-remain.html')

    return advice

def _get_analysis(results) -> Analysis:
    outcomes = group_by_frequency(results)

    if not any(clfy.remain_can_win for clfy in outcomes.keys()):
        return Analysis(
            template='leave.html')

    if all(clfy.remain_can_win and not clfy.alliance_helpful for clfy in outcomes.keys()):
        return Analysis(
            template='remain.html')

    if not any(clfy.alliance_helpful for clfy in outcomes.keys()):
        # eg: speaker's constituency and other strange edge-cases
        return Analysis(
            template='remain-or-leave-no-alliance.html')

    leading_remain_party = set(
        clfy.remain_allicance_leader
        for clfy in outcomes.keys()
        if clfy.remain_allicance_leader is not None)

    chance_of_success = sum(
        ratio
        for clfy, ratio in outcomes.items()
        if clfy.remain_can_win)

    if len(leading_remain_party) == 1:
        party = tuple(leading_remain_party)[0]
        if chance_of_success < 0.5:
            return Analysis(
                template='no-conflict-hard.html',
                we_recommend_party=get_party(party))
        return Analysis(
            template='no-conflict-easy.html',
            we_recommend_party=get_party(party))

    # no single party to back
    return Analysis(
        template='alliance-mixed.html')
