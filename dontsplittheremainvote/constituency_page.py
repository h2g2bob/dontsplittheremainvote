from .advice import get_advice
from .advice import outcome_frequency
from .constituency import all_constituencies
from .constituency import Constituency
from .dataset import Dataset
from .other_sites import OtherSiteSuggestion
from .ppc import PPC
from .result import Result
from collections import defaultdict
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Tuple

class ConstituencyPage(NamedTuple):
    constituency: Constituency
    datasets: Dict[Dataset, Result]
    other_site_suggestions: List[OtherSiteSuggestion]
    known_ppc: List[PPC]

    @property
    def advice(self):
        return get_advice(self.datasets.values(), self.constituency)

    @property
    def outcomes(self):
        return outcome_frequency(self.datasets.values())

    def most_winning_remain_party(self):
        """Which remain party has the most "wins" or "wins if we have an alliance"
        (This gives a weak suggestion of who we would suggest people vote for)
        """
        remain_wins_per_party = defaultdict(int)
        for result in self.datasets.values():
            main_remain_party = result.classify.remain_allicance_leader_as_party()
            if main_remain_party is not None:
                remain_wins_per_party[main_remain_party] += 1
        total = float(sum(remain_wins_per_party.values()))
        over_half_remain_wins = [
            party
            for party, count in remain_wins_per_party.items()
            if count / total > 0.5]
        if over_half_remain_wins:
            [main_remain_party] = over_half_remain_wins
            return main_remain_party
        else:
            return None

    def as_json(self):
        return {
            'constituency': self.constituency.as_json(),
            'advice': self.advice.as_json(),
            'outcome_frequency': [
                [classify_result.as_json(), outcome_freq]
                for classify_result, outcome_freq in self.outcomes],
            'other_sites': [
                other_site_suggestion.as_json()
                for other_site_suggestion in self.other_site_suggestions],
        }
