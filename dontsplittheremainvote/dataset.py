from dataclasses import dataclass
from typing import Callable
from typing import Dict
from .constituency import Constituency
from .result import Result

@dataclass
class Dataset:
    code: str
    title: str
    longdesc: str
    datafunc: Callable[[], Dict[Constituency, Result]]
    _data: Dict[Constituency, Result] = None
    election_result: bool = False

    @property
    def results_by_constituency(self) -> Dict[Constituency, Result]:
        if self._data is None:
            self._data = self.datafunc()
        return self._data

    def __hash__(self):
        return hash(self.code)

    def __cmp__(self, other):
        return cmp(self, other)
