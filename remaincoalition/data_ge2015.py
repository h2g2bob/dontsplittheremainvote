from csv import DictReader
from collections import defaultdict
from .party import get_party
from .constituency import get_constitiuency
from .result import Result
from .dataset import Dataset

DESCRIPTION = Dataset(name='ge2015', description='ge2015')

def _results_by_constituency():
    raw_data = defaultdict(dict)

    with open('data/ge2015/hocl-ge2015-results-full.csv', 'r') as f:
        csvf = DictReader(f)
        for row in csvf:
            constituency = row['ons_id']
            party = row['party_name']
            votes = float(row['share'])
            raw_data[constituency][party] = votes

    return {
        get_constitiuency(constituency_id): Result({
            get_party(party_name): vote_share
            for party_name, vote_share in constituency_results.items()})
        for constituency_id, constituency_results in raw_data.items()}

def get_data():
    return _results_by_constituency()

if __name__ == '__main__':
    print(get_data())
