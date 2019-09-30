from collections import defaultdict
from typing import List
from typing import Dict
from typing import Tuple
import operator

from .result import Result
from .classify import ClassifyResult

def group_by_frequency(results: List[Result]) -> Dict[ClassifyResult, float]:
    classify_frequency = defaultdict(float)
    for result in results:
        classify_frequency[result.classify] += (1.0 / len(results))
    return dict(classify_frequency)

def outcome_frequency(results: List[Result]) -> List[Tuple[ClassifyResult, float]]:
    classify_frequency = list(group_by_frequency(results).items())
    classify_frequency.sort(key=operator.itemgetter(1), reverse=True)
    return classify_frequency

def get_advice(results):
    outcomes = group_by_frequency(results)

    if not any(clfy.remain_can_win for clfy in outcomes.keys()):
        return 'no-remain-win'

    if all(clfy.remain_can_win and not clfy.alliance_helpful for clfy in outcomes.keys()):
        return 'remain-win-certain'

    if not any(clfy.alliance_helpful for clfy in outcomes.keys()):
        # eg: speaker's consituency and other strange edge-cases
        return 'alliance-not-helpful'

    leading_remain_party = set(
        clfy.remain_allicance_leader
        for clfy in outcomes.keys()
        if clfy.remain_allicance_leader is not None)

    chance_of_success = sum(
        ratio
        for clfy, ratio in outcomes.items()
        if clfy.remain_can_win)

    if len(leading_remain_party) == 1:
        if chance_of_success < 0.5:
            return 'alliance-clear-hard-' + repr(leading_remain_party)
        return 'alliance-clear-' + repr(leading_remain_party)

    if chance_of_success < 0.5:
        return 'alliance-mixed-hard'
    return 'alliance-mixed'
