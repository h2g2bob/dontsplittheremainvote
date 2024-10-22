from __future__ import annotations

from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Tuple

from .party import Party
from .party import get_party
from .party import ALLIANCE
from .party import CLAIREWRIGHT
from .party import CON
from .party import DUP
from .party import GREEN
from .party import INDEPENDENT
from .party import LAB
from .party import LD
from .party import NHAP
from .party import OTHERS
from .party import PLAID
from .party import SDLP
from .party import SF
from .party import SNP
from .party import SPEAKER
from .party import UKIP
from .party import UUP
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

    def biggest_remain_party(self):
        [party, _ratio] = self.remainers()[0]
        return party

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

    def description(self) -> str:
        return self.classify.describe(self)

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
            if winner == SDLP:
                    return classify.REMAIN_VICTORY_SDLP
            if winner == ALLIANCE:
                    return classify.REMAIN_VICTORY_ALLIANCE
            if winner == CLAIREWRIGHT:
                    return classify.REMAIN_VICTORY_CLAIREWRIGHT
            raise ValueError(winner)

        rainbow_alliance_share = self.rainbow_alliance_share()
        if rainbow_alliance_share > self.winner_share():
            [remain1, _ratio] = self.remainers()[0]
            if remain1 == LAB:
                return classify.ALLIANCE_LAB
            if remain1 == LD:
                return classify.ALLIANCE_LD
            if remain1 == SNP:
                return classify.ALLIANCE_SNP
            if remain1 == ALLIANCE:
                return classify.ALLIANCE_ALLIANCE
            if remain1 == GREEN:
                return classify.ALLIANCE_GREEN
            if remain1 == NHAP:
                return classify.ALLIANCE_NHAP
            if remain1 == PLAID:
                return classify.ALLIANCE_PLAID
            if remain1 == SDLP:
                return classify.ALLIANCE_SDLP
            if remain1 == CLAIREWRIGHT:
                return classify.ALLIANCE_CLAIREWRIGHT
            if remain1 == SF:
                return classify.ALLIANCE_SF
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
