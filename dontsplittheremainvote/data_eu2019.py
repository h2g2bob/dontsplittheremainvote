from csv import DictReader
from collections import defaultdict
from .party import get_party
from .constituency import get_constitiuency
from .result import Result
from .dataset import Dataset
from . import party

DESCRIPTION = Dataset(name='EU 2019 Estimates', description='European Parliament 2019 (estimated)')
FILE = 'data/eu2019/Estimates of the EP2019 vote in Westminster constituencies - export.csv'

PARTIES = [
    (party.UKIP, 'BRX_pct'),
    (party.CON, 'CON_pct'),
    (party.GREEN, 'GRN_pct'),
    (party.LAB, 'LAB_pct'),
    (party.LD, 'LD_pct'),
    (party.PLAID, 'PC_pct'),
    (party.SNP, 'SNP_pct'),
    (party.OTHERS, 'Other_pct'),
]

def _results_by_constituency():
    raw_data = defaultdict(dict)

    with open(FILE, 'r') as f:
        csvf = DictReader(f)
        for row in csvf:
            constituency = row['PCON11CD']
            for party_name, colname_pc in PARTIES:
                    party = party_name
                    votes = float(row[colname_pc])
                    raw_data[constituency][party] = votes

    return {
        get_constitiuency(constituency_id): Result({
            party: vote_share
            for party, vote_share in constituency_results.items()})
        for constituency_id, constituency_results in raw_data.items()}

def get_data():
    return _results_by_constituency()

if __name__ == '__main__':
    print(get_data())
