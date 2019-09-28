from typing import Namedtuple

class Party(NamedTuple):
    code: str
    remain: bool = False
    color: str = '#000000'

_PARTIES = {
    p.code: p
    for p in [
        Party('LAB', remain=True, color='#FF0000'),
        Party('LD', remain=True, color='#FFFF00'),
        Party('CON', remain=False, color='#0000FF'),
    ]
}

def get(code):
    try:
        return _PARTIES[code]
    except KeyError:
        _PARTIES[code] = Party(code)
        return _PARTIES[code]
