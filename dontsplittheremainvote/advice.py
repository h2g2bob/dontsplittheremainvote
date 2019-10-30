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

class Advice(NamedTuple):
    image: str
    template: str = 'constituency.html'
    advice_kwargs: dict = {}
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

def get_advice(results, constituency) -> Advice:
    # if constituency.slug == 'belfast-south':
    #     return Advice(
    #         image='error.png',
    #         template='contradict.html')
    if constituency.slug == 'don-valley':
        return Advice(
            image='error.png',
            template='special-labour-leave.html',
            advice_kwargs={
                'real_remain': LD,
                'current_mp': 'Caroline Flint'})

    advice = _get_advice(results)

    INDEPENDENT_REMAIN = {
        'broxtowe': CHANGEUK,
        'beaconsfield': INDEPENDENT,
        'eddisbury': INDEPENDENT,
        'runnymede-and-weybridge': INDEPENDENT,
        'south-west-hertfordshire': INDEPENDENT,
    }
    if constituency.slug in INDEPENDENT_REMAIN:
        return Advice(
            image='other.png',
            template='special-independent-remain.html',
            advice_kwargs={
                'party': INDEPENDENT_REMAIN[constituency.slug]})

    # Override our recomendation?
    # SLIGHT_LAB_POLL_BUT_LD_RECOMMEND = []
    # if constituency.slug in SLIGHT_LAB_POLL_BUT_LD_RECOMMEND and advice.template == 'alliance-lab.html':
    #     return Advice(
    #         image='difficult-alliance.png',
    #         template='special-ignore-polling.html',
    #         advice_kwargs={
    #             'we_said': LAB,
    #             'they_said': LD})

    return advice

def _get_advice(results) -> Advice:
    outcomes = group_by_frequency(results)

    if not any(clfy.remain_can_win for clfy in outcomes.keys()):
        return Advice(
            image='leave.png',
            template='leave.html')

    if all(clfy.remain_can_win and not clfy.alliance_helpful for clfy in outcomes.keys()):
        return Advice(
            image='remain.png',
            template='remain.html')

    if not any(clfy.alliance_helpful for clfy in outcomes.keys()):
        # eg: speaker's constituency and other strange edge-cases
        return Advice(
            image='other.png',
            template='other.html')

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
            return Advice(
                image='difficult-alliance.png',
                template='alliance-{}.html'.format(party),
                advice_kwargs={'difficult_win': True},
                we_recommend_party=get_party(party))
        return Advice(
            image='alliance-{}.png'.format(party),
            template='alliance-{}.html'.format(party),
            advice_kwargs={'difficult_win': False},
            we_recommend_party=get_party(party))

    # no single party to back
    return Advice(
        image='difficult-alliance.png',
        template='alliance-mixed.html')
