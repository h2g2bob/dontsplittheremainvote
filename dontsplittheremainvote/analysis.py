from collections import defaultdict
from typing import List
from typing import Dict
from typing import NamedTuple
from typing import Optional
from typing import Tuple
import operator

from . import data_ge2017
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
    we_recommend_party: Optional[Party] = None
    suppressed_party: Optional[Party] = None

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

def get_analysis(datasets, constituency) -> Analysis:
    if constituency.slug == 'don-valley':
        return Analysis(
            template='special-labour-leave.html',
            we_recommend_party=None)

    if constituency.slug == 'buckingham':
        return Analysis(
            template='special-speker-constituency.html')

    results = datasets.values()
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

    if advice.we_recommend_party is not None:
        # Don't Split is wrong to suggest LD here, as LAB dominated the GE2017:
        # https://dontsplittheremainvote.com/constituency/the-wrekin.html
        # The recent EP result suggests LD *could* win... but that's not certain
        # and is probably controversial.
        #
        # This code will suppress suggestions like this, by checking whether the
        # party we recommend has an ok share in 2017 or not. (Not a majority, just
        # not outnumbered 2:1!)
        #
        # This will also suppress places like this:
        # https://dontsplittheremainvote.com/constituency/beckenham.html
        # where the LAB vote share collapsed completely in the European elections.
        #
        # But this is probably ok, because when we suppress a recommendation it
        # just means we rely on our external sources, which will need to deal with
        # this question instead (good luck!)
        general_election_results = datasets[data_ge2017.DATA_2017]
        vote_share_of_recommend_party = general_election_results.results.get(advice.we_recommend_party)
        if vote_share_of_recommend_party is None:
            vote_share_of_recommend_party = 0.0
        vote_share_of_remain_parties = sum(share for _party, share in general_election_results.remainers())
        if vote_share_of_recommend_party / vote_share_of_remain_parties < 0.3:
            return Analysis(
                template='suppressed-too-far-behind-2017.html',
                suppressed_party=advice.we_recommend_party)

        # We conflict with the only other suggestion in
        # https://dontsplittheremainvote.com/constituency/new-forest-east.html
        if constituency.slug == 'new-forest-east':
            return Analysis(
                template='suppressed-manual-avoid-split.html',
                suppressed_party=advice.we_recommend_party)

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
