import json
from collections import defaultdict
from typing import NamedTuple
from typing import List
from typing import Dict
from .constituency import Constituency
from .constituency import get_constitiuency
from .constituency import get_constitiuency_from_slug
from .party import Party
from .party import get_party
from .party import LAB
from .party import LD

class OtherSiteSuggestion(NamedTuple):
    who_suggests: str
    party: Party
    url: str


def _tacticalvote():
    with open('data/tacticalvote/recommendations.json') as f:
        data = json.load(f)
        for recomend in data:
            if recomend['VoteFor'] != 'TBC':
                suggestion = OtherSiteSuggestion(
                    who_suggests='tacticalvote.co.uk',
                    party=get_party(recomend['VoteFor']),
                    url='https://tacticalvote.co.uk/#{}'.format(recomend['Constituency'].replace(' ', '')))
                yield get_constitiuency(recomend['id']), suggestion

def _essex_against_tories():
    results = [
        ('basildon-and-billericay', LAB),
        ('braintree', None),
        ('brentwood-and-ongar', LD),
        ('castle-point', LAB),
        ('chelmsford', LD),
        ('clacton', LAB),
        ('colchester', LD),
        ('epping-forest', LD),
        ('harlow', LAB),
        ('harwich-and-north-essex', None),
        ('maldon', LD),
        ('rayleigh-and-wickford', None),
        ('rochford-and-southend-east', LAB),
        ('saffron-walden', LD),
        ('south-basildon-and-east-thurrock', LAB),
        ('southend-west', None),
        ('thurrock', LAB),
        ('witham', LD)]
    for slug, party in results:
        if party is not None:
            yield [
                get_constitiuency_from_slug(slug),
                OtherSiteSuggestion(
                    who_suggests='Essex Against The Tories',
                    party=party,
                    url='https://twitter.com/ProgEssex/status/1183701065390313472')]

def _early_pv():
    results = [
        ('cheadle', LD),
	('chingford-and-woodford-green', LAB),
	('corby', LAB),
	('hazel-grove', LD),
	('hendon', LAB),
	('north-devon', LD),
	('richmond-park', LD),
	('st-ives', LD),
	('st-albans', LD),
	('wells', LD),

	('bishop-auckland', LAB),
	('canterbury', LAB),
	('carshalton-and-wallington', LD),
	('enfield-southgate', LAB),
	('gedling', LAB),
	('ipswich', LAB),
	('oxford-west-and-abingdon', LD),
	('stroud', LAB),
	('wakefield', LAB),
	('weaver-vale', LAB)]
    for slug, party in results:
        if party is not None:
            yield [
                get_constitiuency_from_slug(slug),
                OtherSiteSuggestion(
                    who_suggests='People\'s Vote (early indication)',
                    party=party,
                    url='https://www.theneweuropean.co.uk/top-stories/tactical-voting-for-a-second-referendum-general-election-1-6261308')]

def get_other_site_suggestions() -> Dict[Constituency, List[OtherSiteSuggestion]]:
    out = defaultdict(list)
    for constituency, suggest in _tacticalvote():
        out[constituency].append(suggest)
    for constituency, suggest in _early_pv():
        out[constituency].append(suggest)
    for constituency, suggest in _essex_against_tories():
        out[constituency].append(suggest)
    return dict(out)
