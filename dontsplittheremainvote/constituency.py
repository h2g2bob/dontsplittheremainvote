import re
from csv import DictReader
from typing import List
from typing import NamedTuple
from typing import Tuple
from collections import defaultdict

COUNTRIES = {
    'Northern Ireland',
    'Scotland',
    'England',
    'Wales'}

class Constituency(NamedTuple):
    ons_id: str
    name: str
    country: str
    region: str
    county: str
    lng_lat: Tuple[float, float]

    @property
    def slug(self):
        return '-'.join(self.name.split()).lower().replace(',', '').replace('.', '')

    @property
    def hashtag(self):
        return ''.join(word.title() for word in self.name.replace(',', '').replace('.', '').split())

    def as_json(self):
        return {
            'name': self.name,
            'slug': self.slug,
            'hashtag': self.hashtag,
            'ons_id': self.ons_id,
            'country': self.country,
            'region': self.region,
            'county': self.county,
        }


def _geo():
    lng_lats = {}
    with open('data/locations/query.csv', 'r') as f:
        csvf = DictReader(f)
        for row in csvf:
            lng, lat = re.compile(r'^Point\(([-0-9\.]+) ([-0-9\.]+)\)$').search(row['geo']).groups()
            lng_lats[row['gss']] = (float(lng), float(lat))
    return lng_lats


_CONSTITUENCIES = {}
def _load_constitency_data():
    constituencies = defaultdict(dict)
    geo = _geo()
    with open('data/ge2017/HoC-GE2017-results-by-candidate.csv', 'r') as f:
        csvf = DictReader(f)
        for row in csvf:
            try:
                lng_lat = geo[row['ons_id']]
            except KeyError:
                print("No lng_lat coordinates: {}".format(row['ons_id']))
                lng_lat = (0.0, 0.0)

            constituency = Constituency(
                ons_id=row['ons_id'],
                name=row['constituency_name'],
                country=row['country_name'],
                region=row['region_name'],
                county=row['county_name'],
                lng_lat=lng_lat)
            assert constituency.country in COUNTRIES, constituency
            constituencies[constituency.ons_id] = constituency
    _CONSTITUENCIES.update(constituencies)

def _normalize_consituency_name(name):
    return re.compile('[^a-z]+').sub('', name.lower())

def get_constitiuency_from_name(name):
    for con in all_constituencies():
        if _normalize_consituency_name(con.name) == _normalize_consituency_name(name):
            return con
    raise ValueError(name)

def get_constitiuency_from_slug(slug):
    for con in all_constituencies():
        if con.slug == slug:
            return con
    raise ValueError(slug)

def get_constitiuency(ons_id):
    if not _CONSTITUENCIES:
        _load_constitency_data()
    return _CONSTITUENCIES[ons_id]

def all_constituencies() -> List[Constituency]:
    if not _CONSTITUENCIES:
        _load_constitency_data()
    return _CONSTITUENCIES.values()
