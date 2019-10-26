from .advice import get_advice
from .advice import outcome_frequency
from .constituency import all_constituencies
from .constituency import Constituency
from .dataset import Dataset
from .other_sites import OtherSiteSuggestion
from .result import Result
from typing import Dict
from typing import List
from typing import NamedTuple

class ConstituencyPage(NamedTuple):
    constituency: Constituency
    datasets: Dict[Dataset, Result]
    other_site_suggestions: List[OtherSiteSuggestion]

    @property
    def advice(self):
        return get_advice(self.datasets.values(), self.constituency)

    @property
    def outcomes(self):
        return outcome_frequency(self.datasets.values())

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
