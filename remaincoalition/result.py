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
from .party import SPEAKER

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
                pass
        sum_votes = results.values()
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

    def would_rainbow_win(self) -> bool:
        total_remain_vote = sum(ratio for _party, ratio in self.remainers())
        return total_remain_vote > 0.5

    def classify(self) -> Tuple[str, Party]:
        # XXX how to combine results together?
        winner = self.winner()
        if winner.remain:
            return ('remain-victory', winner)
        if self.would_rainbow_win():
            [biggest_remain, _ratio] = self.remainers()[0]
            return ('alliance-needed', biggest_remain)
        return ('difficult', winner)

    def classify_logo(self) -> str:
        winner = self.winner()

        if winner == SPEAKER:
            return 'speaker'

        if winner.remain:
            if winner == LAB:
                    return 'remain-victory-lab'
            if winner == LD:
                    return 'remain-victory-ld'
            if winner == SNP:
                    return 'remain-victory-snp'
            if winner == PLAID:
                    return 'remain-victory-plaid'
            if winner == SF:
                    return 'remain-victory-sf'
            if winner == GREEN:
                    return 'remain-victory-green'
            print(repr(['win', winner]))
            return 'remain-victory'

        if self.would_rainbow_win():
            remainers = [party for party, _ratio in self.remainers()]
            [remain1, remain2] = remainers[:2]
            if remain1 == LAB and remain2 == LD:
                return 'alliance-needed-lab-ld'
            if remain1 == LAB and remain2 == PLAID:
                return 'alliance-needed-lab-plaid'
            if remain1 == LD and remain2 == LAB:
                return 'alliance-needed-ld-lab'
            if remain1 == SNP and remain2 == LAB:
                return 'alliance-needed-snp-lab'
            if remain1 == SF and remain2 == ALLIANCE:
                return 'alliance-needed-sf-alliance'
            if remain1 == LAB and remain2 == ALLIANCE:
                return 'alliance-needed-lab-alliance'
            print(repr(['a', remain1, remain2]))
            return 'alliance-needed'

        if winner == CON:
            return 'difficult-con'
        if winner == DUP:
            return 'difficult-dup'

        print(repr(['d', winner]))
        return 'difficult'
