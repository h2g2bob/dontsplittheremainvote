from csv import DictReader
from collections import defaultdict
from typing import NamedTuple
from .constituency import get_constitiuency_from_name
from .party import Party
from .party import CHANGEUK
from .party import DOMINICGRIEVE
from .party import GREEN
from .party import INDEPENDENT
from .party import LAB
from .party import LD
from .party import PLAID

FILENAME='data/pacts/Pacts _ Parties Standing Down in GE2019 - GB Pacts.csv'
PARTY = {
    'GRN': GREEN,
    'IGC': CHANGEUK,
    'IND (Grieve)': DOMINICGRIEVE,
    'IND': INDEPENDENT,
    'LAB': LAB,
    'LDM': LD,
    'PLC': PLAID,
}

class Pact(NamedTuple):
    down: Party
    support: Party

    def as_json(self):
        return {
            'down': self.down.short,
            'support': self.support.short}

_CONSTITUENCY_CORRECTIONS = {
    'Bermondsy & Old Southwark': 'Bermondsey and Old Southwark',
    'Brighton Pavillion': 'Brighton Pavilion',
    'Carmarthen East': 'Carmarthen East and Dinefwr',
    'Dwyfor Meirionydd': 'Dwyfor Meirionnydd',
    'Penistone & Stockbridge': 'Penistone and Stocksbridge',
    'Thornberry & Yate': 'Thornbury and Yate',
    'Ynys Môn': 'Ynys Mon',
}
def get_pacts():
    pacts = defaultdict(list)
    with open(FILENAME, 'r') as f:
        csvf = DictReader(f)
        for row in csvf:
            cname = row['Constituency']
            cname = _CONSTITUENCY_CORRECTIONS.get(cname, cname)
            constituency = get_constitiuency_from_name(cname)
            pacts[constituency].append(Pact(
                down=PARTY[row['Standing Down']],
                support=PARTY[row['Implied Support']]))
    return pacts
