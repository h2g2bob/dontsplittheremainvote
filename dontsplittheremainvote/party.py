from typing import NamedTuple

class Party(NamedTuple):
    code: str
    remain: bool = False
    color: str = '#000000'
    short: str = 'other'

    @property
    def name(self):
        return self.code

OTHERS = Party('Others', remain=False, color='#999999')
LAB = Party('Labour', remain=True, color='#DC241F', short='lab')
LD = Party('Liberal Democrat', remain=True, color='#FAA61A', short='ld')
SNP = Party('Scottish National Party', remain=True, color='#FFF95D', short='snp')
CON = Party('Conservative', remain=False, color='#0087DC')
PLAID = Party('Plaid Cymru', remain=True, color='#3F8428', short='plaid')
DUP = Party('DUP', remain=False, color='#D46A4C')
ALLIANCE = Party('Alliance', remain=True, color='#F6CB2F', short='alliance')
SF = Party('Sinn Fein', remain=True, color='#008800')
GREEN = Party('Green', remain=True, color='#6AB023', short='green')
UKIP = Party('UKIP / Brexit', remain=False, color='#70147A')
UUP = Party('UUP', remain=False, color='#9999FF')
NHAP = Party('National Health Action Party', remain=True, color='#0071BB')
SDLP = Party('SDLP', remain=True, color='#3A9E84', short='sdlp')
INDEPENDENT = Party('Independent', remain=False, color='#CCCCCC')
SPEAKER = Party('Speaker', remain=True, color='#888888')

_ALL_PARTIES = [
    LAB,
    LD,
    SNP,
    CON,
    PLAID,
    DUP,
    SF,
    ALLIANCE,
    GREEN,
    UKIP,
    UUP,
    NHAP,
    SDLP,
    INDEPENDENT,
    SPEAKER,
    Party('The Yorkshire Party', remain=False, color='#00AEEF'),
    OTHERS,
]

_PARTIES_BY_CODE = {
    p.code: p
    for p in _ALL_PARTIES}

_PARTIES_BY_SHORT = {
    p.short: p
    for p in _ALL_PARTIES
    if p.short}

_MAPPINGS = {
    'Labour and Co-operative': 'Labour',
    'Democratic Unionist Party': 'DUP',
    'Ulster Unionist Party': 'UUP',
    'UK Independence Party': 'UKIP / Brexit',
    'Lib Dem': 'Liberal Democrat',
    'SNP': 'Scottish National Party',
    'Social Democratic and Labour Party': 'SDLP',

    # tacticalvote mis-spelling
    'Labout': 'Labour',
}

def get_party(code):
    try:
        return _PARTIES_BY_CODE[_MAPPINGS.get(code, code)]
    except KeyError:
        try:
            return _PARTIES_BY_SHORT[_MAPPINGS.get(code, code)]
        except KeyError:
            print('Adding {}'.format(code))
            _PARTIES_BY_CODE[code] = Party(code)
            return _PARTIES_BY_CODE[code]
