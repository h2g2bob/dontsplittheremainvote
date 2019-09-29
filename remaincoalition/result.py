from __future__ import annotations

from typing import NamedTuple
from typing import Dict

from .party import Party
from .party import OTHERS
from .party import get_party

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
