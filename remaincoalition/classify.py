from __future__ import annotations

from typing import Dict
from typing import List
from typing import NamedTuple
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

class _RemainVictory(ClassifyResult):
    def __new__(self, shortname, longname):
        return super().__new__(self, logo=f'remain-victory-{shortname}', name=f'Remain win: {longname}')

class _LeaveVictory(ClassifyResult):
    def __new__(self, shortname, longname):
        return super().__new__(self, logo=f'difficult-{shortname}', name=f'Largest party is {longname}, and an alliance would not have helped here.')

class _AllianceNeeded(ClassifyResult):
    def __new__(self, short1, short2, long1):
        return super().__new__(self, logo=f'remain-victory-{short1}-{short2}', name=f'Remain can win if parties work together. The largest party is {long1}.')

REMAIN_VICTORY_LAB = _RemainVictory('lab', 'Labour')
REMAIN_VICTORY_LD = _RemainVictory('ld', 'Liberal Democrats')
REMAIN_VICTORY_SNP = _RemainVictory('snp', 'SNP')
REMAIN_VICTORY_PLAID = _RemainVictory('plaid', 'Plaid Cymru')
REMAIN_VICTORY_SF = _RemainVictory('sf', 'Sinn Fenn')
REMAIN_VICTORY_GREEN = _RemainVictory('green', 'Green')

ALLIANCE_NEEDED_LAB_LD = _AllianceNeeded('lab', 'ld', 'Labour')
ALLIANCE_NEEDED_LAB_PLAID = _AllianceNeeded('lab', 'plaid', 'Labour')
ALLIANCE_NEEDED_LAB_ALLIANCE = _AllianceNeeded('lab', 'alliance', 'Labour')
ALLIANCE_NEEDED_LD_LAB = _AllianceNeeded('ld', 'lab', 'Liberal Democrats')
ALLIANCE_NEEDED_SNP_LAB = _AllianceNeeded('snp', 'lab', 'SNP')
SF_ALLIANCE = ClassifyResult(logo='other', name=f'Remain can win if parties work together. The largest party is Sinn Fenn, but Sinn Fenn do not take their seats in the UK Parliament.')

DIFFICULT_CON = _LeaveVictory('con', 'Conservative')
DIFFICULT_DUP = _LeaveVictory('dup', 'DUP')
DIFFICULT_UUP = _LeaveVictory('dup', 'UUP')
DIFFICULT_UKIP = _LeaveVictory('ukip', 'UKIP')

OTHER = ClassifyResult(logo='other', name=f'Unusual result')
