from typing import NamedTuple

class Party(NamedTuple):
    code: str
    remain: bool = False
    color: str = '#000000'
    short: str = 'other'

    @property
    def name(self):
        return self.code

OTHERS = Party('Others', remain=False, color='#CCCCCC')
LAB = Party('Labour', remain=True, color='#DC241F', short='lab')
LD = Party('Liberal Democrat', remain=True, color='#FAA61A', short='ld')
SNP = Party('Scottish National Party', remain=True, color='#FFF95D', short='snp')
CON = Party('Conservative', remain=False, color='#0087DC')
CHANGEUK = Party('Change UK', remain=False, color='#222222', short='chuk')
PLAID = Party('Plaid Cymru', remain=True, color='#3F8428', short='plaid')
DUP = Party('DUP', remain=False, color='#D46A4C')
ALLIANCE = Party('Alliance', remain=True, color='#F6CB2F', short='alliance')
SF = Party('Sinn Fein', remain=True, color='#008800', short='sf')
GREEN = Party('Green', remain=True, color='#6AB023', short='green')
UKIP = Party('UKIP / Brexit', remain=False, color='#70147A')
UUP = Party('UUP', remain=False, color='#9999FF')
NHAP = Party('National Health Action Party', remain=True, color='#0071BB')
SDLP = Party('SDLP', remain=True, color='#3A9E84', short='sdlp')
CLAIREWRIGHT = Party('Claire Wright', remain=True, color='#00bd93', short='ind-wright')
INDEPENDENT = Party('Independent', remain=False, color='#e7e7e7', short='ind')
ANNASOUBRY = Party('Anna Soubry', remain=False, color='#222222', short='chuk')
DOMINICGRIEVE = Party('Dominic Grieve', remain=True, color='#e7e7e7', short='ind')
DAVIDGAUKE = Party('David Gauke', remain=True, color='#e7e7e7', short='ind')
GAVINSHUKER = Party('Gavin Shuker', remain=True, color='#e7e7e7', short='ind')
SPEAKER = Party('Speaker', remain=True, color='#888888')
ANYPARTY = Party('any remain party', remain=True, color='#888888', short='any')

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
    CLAIREWRIGHT,
    INDEPENDENT,
    SPEAKER,
    Party('The Yorkshire Party', remain=False, color='#00AEEF'),
    OTHERS,
]

_PARTIES_BY_CODE = {
    p.code: p
    for p in _ALL_PARTIES}

_MAPPINGS = {
    'lab': LAB,
    'snp': SNP,
    'ld': LD,
    'alliance': ALLIANCE,
    'plaid': PLAID,

    'Labour and Co-operative': LAB,
    'Democratic Unionist Party': DUP,
    'Ulster Unionist Party': UUP,
    'UK Independence Party': UKIP,
    'Lib Dem': LD,
    'SNP': SNP,
    'Social Democratic and Labour Party': SDLP,

    # tacticalvote mis-spelling
    'Labout': LAB,

    'Labour Party': LAB,
    'The Brexit Party': UKIP,
    'Liberal Democrats': LD,
    'Scottish National Party (SNP)': SNP,
    'Green Party': GREEN,
    'Conservative and Unionist Party': CON,
    'Sinn Féin': SF,
    'Alliance Party of Northern Ireland': ALLIANCE,
    'Social Democratic & Labour Party': SDLP,
    'UK Independence Party (UKIP)': UKIP,
    'The Independent Group for Change': CHANGEUK,
    'Labour and Co-operative Party': LAB,
    'Plaid Cymru - The Party of Wales': PLAID,
    'Scottish Green Party': GREEN,
    'Alliance - Alliance Party of Northern Ireland': ALLIANCE,
    'SDLP (Social Democratic & Labour Party)': SDLP,
    'Speaker seeking re-election': SPEAKER,
    'Democratic Unionist Party - D.U.P.': DUP,
}

def get_party(code):
    try:
        return _PARTIES_BY_CODE[code]
    except KeyError:
        try:
            return _MAPPINGS[code]
        except KeyError:
            print('Adding {}'.format(code))
            _PARTIES_BY_CODE[code] = Party(code)
            return _PARTIES_BY_CODE[code]
