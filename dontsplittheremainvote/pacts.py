from csv import DictReader
from collections import defaultdict
from typing import NamedTuple
from .constituency import get_constitiuency_from_name
from .party import Party
from .party import ANYPARTY
from .party import CHANGEUK
from .party import DOMINICGRIEVE
from .party import GREEN
from .party import INDEPENDENT
from .party import LAB
from .party import LD
from .party import PLAID
from .party import SNP

FILENAME='data/pacts/Pacts _ Parties Standing Down in GE2019 - GB Pacts.csv'
PARTY = {
    'GRN': GREEN,
    'IGC': CHANGEUK,
    'IND': INDEPENDENT,
    'IND (Beavis)': INDEPENDENT,
    'IND (Grieve)': DOMINICGRIEVE,
    'LAB': LAB,
    'LDM': LD,
    'PLC': PLAID,
    'SNP': SNP,
    'N/A (LAB)': ANYPARTY,
    'N/A': ANYPARTY,
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
            if cname == 'ALL GE2017 CON SEATS':
                continue
            constituency = get_constitiuency_from_name(cname)
            pacts[constituency].append(Pact(
                down=PARTY[row['Standing Down'].strip()],
                support=PARTY[row['Implied Support'].strip()]))
    return pacts
