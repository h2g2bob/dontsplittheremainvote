from csv import DictReader
from typing import NamedTuple
from collections import defaultdict

class Constituency(NamedTuple):
    ons_id: str
    name: str

    @property
    def slug(self):
        return '-'.join(self.name.split()).lower().replace(',', '').replace('.', '')

    @property
    def hashtag(self):
        return '#' + ''.join(word.title() for word in self.name.replace(',', '').replace('.', '').split())

_CONSTITUENCIES = {}
def _load_constitency_data():
    constituencies = defaultdict(dict)
    with open('data/ge2017/HoC-GE2017-results-by-candidate.csv', 'r') as f:
        csvf = DictReader(f)
        for row in csvf:
            constituency = Constituency(
                ons_id=row['ons_id'],
                name=row['constituency_name'])
            constituencies[constituency.ons_id] = constituency
    _CONSTITUENCIES.update(constituencies)

def get_constitiuency_from_slug(slug):
    for con in all_constituencies():
        if con.slug == slug:
            return con
    raise ValueError(slug)

def get_constitiuency(ons_id):
    if not _CONSTITUENCIES:
        _load_constitency_data()
    return _CONSTITUENCIES[ons_id]

def all_constituencies():
    if not _CONSTITUENCIES:
        _load_constitency_data()
    return _CONSTITUENCIES.values()
