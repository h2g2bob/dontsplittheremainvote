from __future__ import annotations

from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Tuple

from .party import Party
from .party import get_party
from .party import CON
from .party import LAB
from .party import LD
from .party import OTHERS
from .party import PLAID
from .party import SNP
from .party import DUP
from .party import SF
from .party import ALLIANCE
from .party import GREEN
from .party import UUP
from .party import NHAP
from .party import SPEAKER
from .party import INDEPENDENT
from .party import UKIP
from . import classify

def _party_ratio_sort(party_and_ratio):
    [party, ratio] = party_and_ratio
    if party == OTHERS:
        return 0
    return ratio

class Result(NamedTuple):
    results: Dict[Party, float]

    def adjust_for_polling(self, adjustments: Dict[Party, float]) -> Result:
        results = self.results.copy()
        for party, adjust in adjustments.items():
            try:
                results[party] += adjust
                if results[party] < 0.0:
                    del results[party]
            except KeyError:
                results[party] = adjust
        sum_votes = sum(results.values())
        normalization = 1.0 / sum_votes
        return Result({
            party: votes * normalization
            for party, votes in results.items()})

    def collect_others(self, threshold: float) -> Result:
        results = {
            party: ratio
            for party, ratio in self.results.items()
            if ratio >= threshold and party != OTHERS}
        results[OTHERS] = 1.0 - sum(results.values())
        return Result(results)

    def remainers(self) -> List[Tuple[Party, float]]:
        party_and_ratio = [
            (party, ratio)
            for party, ratio in self.results.items()
            if party.remain]
        party_and_ratio.sort(key=_party_ratio_sort, reverse=True)
        return party_and_ratio

    def leavers(self) -> List[Tuple[Party, float]]:
        party_and_ratio = [
            (party, ratio)
            for party, ratio in self.results.items()
            if not party.remain]
        party_and_ratio.sort(key=_party_ratio_sort, reverse=True)
        return party_and_ratio

    def winner(self) -> Party:
        [party, _ratio] = max(
            self.results.items(),
            key=_party_ratio_sort)
        return party

    def winner_share(self) -> float:
        return max(self.results.values())

    def rainbow_alliance_share(self) -> float:
        total_remain_vote = sum(ratio for _party, ratio in self.remainers())
        return total_remain_vote

    @property
    def classify(self) -> classify.ClassifyResult:
        winner = self.winner()

        if winner == SPEAKER:
            return classify.OTHER
        if winner == INDEPENDENT:
            return classify.OTHER

        if winner.remain:
            if winner == LAB:
                    return classify.REMAIN_VICTORY_LAB
            if winner == LD:
                    return classify.REMAIN_VICTORY_LD
            if winner == SNP:
                    return classify.REMAIN_VICTORY_SNP
            if winner == PLAID:
                    return classify.REMAIN_VICTORY_PLAID
            if winner == SF:
                    return classify.REMAIN_VICTORY_SF
            if winner == GREEN:
                    return classify.REMAIN_VICTORY_GREEN
            raise ValueError(winner)

        rainbow_alliance_share = self.rainbow_alliance_share()
        if rainbow_alliance_share > 0.5:
            remainers = [party for party, _ratio in self.remainers()]
            [remain1, remain2] = remainers[:2]
            if remain1 == LAB and remain2 == LD:
                return classify.ALLIANCE_NEEDED_LAB_LD
            if remain1 == LAB and remain2 == PLAID:
                return classify.ALLIANCE_NEEDED_LAB_PLAID
            if remain1 == LAB and remain2 == ALLIANCE:
                return classify.ALLIANCE_NEEDED_LAB_ALLIANCE
            if remain1 == LD and remain2 == LAB:
                return classify.ALLIANCE_NEEDED_LD_LAB
            if remain1 == LD and remain2 == GREEN:
                return classify.ALLIANCE_NEEDED_LD_GREEN
            if remain1 == LD and remain2 == PLAID:
                return classify.ALLIANCE_NEEDED_LD_PLAID
            if remain1 == SNP and remain2 == LAB:
                return classify.ALLIANCE_NEEDED_SNP_LAB
            if remain1 == SNP and remain2 == LD:
                return classify.ALLIANCE_NEEDED_SNP_LD
            if remain1 == ALLIANCE and remain2 == SF:
                return classify.ALLIANCE_NEEDED_ALLIANCE_SF
            if remain1 == ALLIANCE and remain2 == LD:
                return classify.ALLIANCE_NEEDED_ALLIANCE_LD
            if remain1 == SF:
                return classify.SF_ALLIANCE
            raise ValueError([remain1, remain2])

        if rainbow_alliance_share > self.winner_share():
            [remain1, _ratio] = self.remainers()[0]
            if remain1 == LAB:
                return classify.DIFFICULT_ALLIANCE_LAB
            if remain1 == LD:
                return classify.DIFFICULT_ALLIANCE_LD
            if remain1 == SNP:
                return classify.DIFFICULT_ALLIANCE_SNP
            if remain1 == ALLIANCE:
                return classify.DIFFICULT_ALLIANCE_ALLIANCE
            if remain1 == GREEN:
                return classify.DIFFICULT_ALLIANCE_GREEN
            if remain1 == NHAP:
                return classify.DIFFICULT_ALLIANCE_GREEN
            if remain1 == SF:
                return classify.SF_ALLIANCE
            raise ValueError(remain1)

        if winner == CON:
            return classify.LEAVE_VICTORY_CON
        if winner == DUP:
            return classify.LEAVE_VICTORY_DUP
        if winner == UUP:
            return classify.LEAVE_VICTORY_UUP
        if winner == UKIP:
            return classify.LEAVE_VICTORY_UKIP
        raise ValueError(winner)
