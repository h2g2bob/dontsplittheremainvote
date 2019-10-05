from .advice import get_advice
from .advice import outcome_frequency
from .constituency import all_constituencies
from .constituency import Constituency
from .dataset import Dataset
from .result import Result
from typing import Dict
from typing import List
from typing import NamedTuple

class ConstituencyPage(NamedTuple):
    constituency: Constituency
    datasets: Dict[Dataset, Result]

    @property
    def advice(self):
        return get_advice(self.datasets.values())

    @property
    def outcomes(self):
        return outcome_frequency(self.datasets.values())

