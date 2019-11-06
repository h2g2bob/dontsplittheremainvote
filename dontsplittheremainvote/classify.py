from __future__ import annotations

from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple

from .party import get_party
from .party import ALLIANCE
from .party import CLAIREWRIGHT
from .party import CON
from .party import DUP
from .party import GREEN
from .party import LAB
from .party import LD
from .party import NHAP
from .party import OTHERS
from .party import PLAID
from .party import SDLP
from .party import SF
from .party import SNP
from .party import SPEAKER

class ClassifyResult(NamedTuple):
    logo: str
    name: str

    remain_allicance_leader: Optional[str]
    remain_can_win: bool
    alliance_helpful: bool

    def remain_allicance_leader_as_party(self):
        if self.remain_allicance_leader is None:
            return None
        return get_party(self.remain_allicance_leader)

    def describe(self, _result):
        return self.name

    def as_json(self):
        return {
            'img': self.logo,
            'text': self.name,
        }


class _RemainVictory(ClassifyResult):
    def __new__(self, shortname, longname):
        return super().__new__(self,
            logo=f'remain-victory-{shortname}',
            name=f'Remain win: {longname}',
            remain_allicance_leader=shortname,
            remain_can_win=True,
            alliance_helpful=False)


class _LeaveVictory(ClassifyResult):
    def __new__(self, shortname, longname):
        return super().__new__(self,
            logo=f'leave-victory-{shortname}',
            name=f'Largest party is {longname}. An alliance would not have helped here.',
            remain_allicance_leader=None,
            remain_can_win=False,
            alliance_helpful=False)

class _NeedAlliance(ClassifyResult):
    def __new__(self, party):
        return super().__new__(self,
            logo='difficult-alliance-{}'.format(party.short),
            name='Remain can win if we work together. The largest party is {}.'.format(party.name),
            remain_allicance_leader=party.short,
            remain_can_win=True,
            alliance_helpful=True)

    def describe(self, result):
        remainers = [pty for pty, _share in result.remainers()]
        big_remain, other_remain_parties = remainers[0], remainers[1:]
        if len(other_remain_parties) == 1:
            small_parties_text = other_remain_parties[0].name
        else:
            small_parties_text = '{} and {}'.format(
                ', '.join(pty.name for pty in other_remain_parties[:-1]),
                other_remain_parties[-1].name)
        return 'Remain wins if {} vote for {}'.format(
            small_parties_text,
            big_remain.name)


REMAIN_VICTORY_LAB = _RemainVictory('lab', 'Labour')
REMAIN_VICTORY_LD = _RemainVictory('ld', 'Liberal Democrats')
REMAIN_VICTORY_SNP = _RemainVictory('snp', 'SNP')
REMAIN_VICTORY_PLAID = _RemainVictory('plaid', 'Plaid Cymru')
REMAIN_VICTORY_SF = _RemainVictory('sf', 'Sinn Fenn')
REMAIN_VICTORY_GREEN = _RemainVictory('green', 'Green')
REMAIN_VICTORY_SDLP = _RemainVictory('sdlp', 'SDLP')
REMAIN_VICTORY_ALLIANCE = _RemainVictory('alliance', 'Alliance')
REMAIN_VICTORY_CLAIREWRIGHT = _RemainVictory('ind-wright', 'Claire Wright')

ALLIANCE_ALLIANCE = _NeedAlliance(ALLIANCE)
ALLIANCE_CLAIREWRIGHT = _NeedAlliance(CLAIREWRIGHT)
ALLIANCE_GREEN = _NeedAlliance(GREEN)
ALLIANCE_LAB = _NeedAlliance(LAB)
ALLIANCE_LD = _NeedAlliance(LD)
ALLIANCE_NHAP = _NeedAlliance(NHAP)
ALLIANCE_PLAID = _NeedAlliance(PLAID)
ALLIANCE_SDLP = _NeedAlliance(SDLP)
ALLIANCE_SNP = _NeedAlliance(SNP)

SF_ALLIANCE = ClassifyResult(
    logo='other',
    name=f'Remain can win if parties work together. The largest party is Sinn Fenn, but Sinn Fenn do not take their seats in the UK Parliament.',
    remain_allicance_leader=None,
    remain_can_win=False,
    alliance_helpful=False)

LEAVE_VICTORY_CON = _LeaveVictory('con', 'Conservative')
LEAVE_VICTORY_DUP= _LeaveVictory('dup', 'DUP')
LEAVE_VICTORY_UUP = _LeaveVictory('uup', 'UUP')
LEAVE_VICTORY_UKIP = _LeaveVictory('ukip', 'UKIP / Brexit')

OTHER = ClassifyResult(
    logo='other',
    name=f'Unusual result',
    remain_allicance_leader=None,
    remain_can_win=False,
    alliance_helpful=False)
