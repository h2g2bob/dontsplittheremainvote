from typing import NamedTuple
from typing import Dict

from .party import Party
from .party import OTHERS
from .party import get_party

class Result(NamedTuple):
    results: Dict[Party, float]

    # def adjust_for_polling()

    def collect_others(self, threshold: float) -> Result:
        results = {
            party: ratio
            for party, ratio in self.results.items()
            if ratio >= threshold and party != OTHERS}
        results[OTHERS] = 1.0 - sum(results.values())
        return Result(results)
