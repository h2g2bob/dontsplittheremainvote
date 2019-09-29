from typing import NamedTuple

class Party(NamedTuple):
    code: str
    remain: bool = False
    color: str = '#000000'

    @property
    def name(self):
        return self.code

OTHERS = Party('OTH', remain=False, color='#999999')
LAB = Party('Labour', remain=True, color='#DC241F')
LD = Party('Liberal Democrat', remain=True, color='#FAA61A')
SNP = Party('Scottish National Party', remain=True, color='#FFF95D')
CON = Party('Conservative', remain=False, color='#0087DC')
PLAID = Party('Plaid Cymru', remain=True, color='#3F8428')
DUP = Party('DUP', remain=False, color='#D46A4C')
ALLIANCE = Party('Alliance', remain=True, color='#F6CB2F')
SF = Party('Sinn Fein', remain=True, color='#008800')
GREEN = Party('Green', remain=True, color='#6AB023')
UKIP = Party('UK Independence Party', remain=False, color='#70147A')
UUP = Party('UUP', remain=False, color='#9999FF')
INDEPENDENT = Party('Independent', remain=False, color='#CCCCCC')
SPEAKER = Party('Speaker', remain=True, color='#888888')

_PARTIES = {
    p.code: p
    for p in [
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
        INDEPENDENT,
        SPEAKER,
        Party('The Yorkshire Party', remain=False, color='#00AEEF'),
        Party('National Health Action Party', remain=True, color='#0071BB'),
        OTHERS,
    ]
}

_MAPPINGS = {
    'Labour and Co-operative': 'Labour',
    'Social Democratic and Labour Party': 'Labour',
    'Democratic Unionist Party': 'DUP',
    'Ulster Unionist Party': 'UUP',
}

def get_party(code):
    try:
        return _PARTIES[_MAPPINGS.get(code, code)]
    except KeyError:
        _PARTIES[code] = Party(code)
        return _PARTIES[code]
