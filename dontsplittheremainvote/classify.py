from __future__ import annotations

from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple

from .party import CON
from .party import LAB
from .party import LD
from .party import OTHERS
from .party import PLAID
from .party import SNP
from .party import DUP
from .party import SF
from .party import ALLIANCE
from .party import GREEN
from .party import SPEAKER

class ClassifyResult(NamedTuple):
    logo: str
    name: str

    remain_allicance_leader: Optional[str]
    remain_can_win: bool
    alliance_helpful: bool


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

class _AllianceNeeded(ClassifyResult):
    def __new__(self, short1, short2, long1):
        return super().__new__(self,
            logo=f'alliance-victory-{short1}-{short2}',
            name=f'Remain can only win if parties work together. The largest party is {long1}.',
            remain_allicance_leader=short1,
            remain_can_win=True,
            alliance_helpful=True)

class _DifficultAlliance(ClassifyResult):
    def __new__(self, short1):
        return super().__new__(self,
            logo=f'difficult-alliance-{short1}',
            name=f'If the leave vote is split, a remain alliance can win.',
            remain_allicance_leader=short1,
            remain_can_win=True,
            alliance_helpful=True)

REMAIN_VICTORY_LAB = _RemainVictory('lab', 'Labour')
REMAIN_VICTORY_LD = _RemainVictory('ld', 'Liberal Democrats')
REMAIN_VICTORY_SNP = _RemainVictory('snp', 'SNP')
REMAIN_VICTORY_PLAID = _RemainVictory('plaid', 'Plaid Cymru')
REMAIN_VICTORY_SF = _RemainVictory('sf', 'Sinn Fenn')
REMAIN_VICTORY_GREEN = _RemainVictory('green', 'Green')
REMAIN_VICTORY_SDLP = _RemainVictory('sdlp', 'SDLP')

ALLIANCE_NEEDED_LAB_LD = _AllianceNeeded('lab', 'ld', 'Labour')
ALLIANCE_NEEDED_LAB_PLAID = _AllianceNeeded('lab', 'plaid', 'Labour')
ALLIANCE_NEEDED_LAB_ALLIANCE = _AllianceNeeded('lab', 'alliance', 'Labour')
ALLIANCE_NEEDED_LAB_GREEN = _AllianceNeeded('lab', 'green', 'Labour')
ALLIANCE_NEEDED_LD_LAB = _AllianceNeeded('ld', 'lab', 'Liberal Democrats')
ALLIANCE_NEEDED_LD_GREEN = _AllianceNeeded('ld', 'green', 'Liberal Democrats')
ALLIANCE_NEEDED_LD_PLAID = _AllianceNeeded('ld', 'plaid', 'Liberal Democrats')
ALLIANCE_NEEDED_LD_SNP = _AllianceNeeded('ld', 'snp', 'Liberal Democrats')
ALLIANCE_NEEDED_SNP_LAB = _AllianceNeeded('snp', 'lab', 'SNP')
ALLIANCE_NEEDED_SNP_LD = _AllianceNeeded('snp', 'ld', 'SNP')
ALLIANCE_NEEDED_ALLIANCE_SF = _AllianceNeeded('alliance', 'sf', 'Alliance')
ALLIANCE_NEEDED_ALLIANCE_LD = _AllianceNeeded('alliance', 'ld', 'Alliance')
ALLIANCE_NEEDED_PLAID_LD = _AllianceNeeded('plaid', 'ld', 'Plaid Cymru')
ALLIANCE_NEEDED_GREEN_LAB = _AllianceNeeded('green', 'lab', 'Green')
ALLIANCE_NEEDED_GREEN_LD = _AllianceNeeded('green', 'ld', 'Green')
ALLIANCE_NEEDED_PLAID_LAB = _AllianceNeeded('plaid', 'lab', 'Plaid Cymru')
ALLIANCE_NEEDED_SDLP_ALLIANCE = _AllianceNeeded('sdlp', 'alliance', 'SDLP')

SF_ALLIANCE = ClassifyResult(
    logo='other',
    name=f'Remain can win if parties work together. The largest party is Sinn Fenn, but Sinn Fenn do not take their seats in the UK Parliament.',
    remain_allicance_leader=None,
    remain_can_win=False,
    alliance_helpful=False)

DIFFICULT_ALLIANCE_LAB = _DifficultAlliance('lab')
DIFFICULT_ALLIANCE_LD = _DifficultAlliance('ld')
DIFFICULT_ALLIANCE_SNP = _DifficultAlliance('snp')
DIFFICULT_ALLIANCE_ALLIANCE = _DifficultAlliance('alliance')
DIFFICULT_ALLIANCE_GREEN = _DifficultAlliance('green')
DIFFICULT_ALLIANCE_NHAP = _DifficultAlliance('nhap')
DIFFICULT_ALLIANCE_PLAID = _DifficultAlliance('plaid')

LEAVE_VICTORY_CON = _LeaveVictory('con', 'Conservative')
LEAVE_VICTORY_DUP= _LeaveVictory('dup', 'DUP')
LEAVE_VICTORY_UUP = _LeaveVictory('dup', 'UUP')
LEAVE_VICTORY_UKIP = _LeaveVictory('ukip', 'UKIP / Brexit')

OTHER = ClassifyResult(
    logo='other',
    name=f'Unusual result',
    remain_allicance_leader=None,
    remain_can_win=False,
    alliance_helpful=False)
