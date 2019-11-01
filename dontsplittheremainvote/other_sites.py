import json
import re
from collections import defaultdict
from typing import NamedTuple
from typing import List
from typing import Dict
from .constituency import Constituency
from .constituency import get_constitiuency
from .constituency import get_constitiuency_from_name
from .constituency import get_constitiuency_from_slug
from .party import Party
from .party import get_party
from .party import ALLIANCE
from .party import CHANGEUK
from .party import INDEPENDENT
from .party import GREEN
from .party import LAB
from .party import LD
from .party import NHAP
from .party import OTHERS
from .party import PLAID
from .party import SDLP
from .party import SF
from .party import SNP

class OtherSiteSuggestion(NamedTuple):
    who_suggests: str
    party: Party
    url: str

    def as_json(self):
        return {
            'who_suggests': self.who_suggests,
            'party': self.party.short,
            'url': self.url,
        }


def _getvoting():
    PARTIES = {
        'Anna Soubry': CHANGEUK,
        'Antoinette Sandbach': INDEPENDENT, # former conservative
        'Claire Wright': INDEPENDENT,
        'David Gauke': INDEPENDENT, # former conservative
        'Dominic Grieve': INDEPENDENT, # former conservative
        'Green': GREEN,
        'Guto Bebb': INDEPENDENT, # former conservative
        'Lab': LAB,
        'Lib Dem': LD,
        'LibLab': None, # "Either LD or LAB"
        'none': None,
        'Philip Hammond': INDEPENDENT, # former conservative
        'Plaid': PLAID,
        'Pledge': None,
    }

    with open('data/getvoting/NewData.json') as f:
        data = json.load(f)
        for ons_id, recomend in data.items():
            constituency = get_constitiuency(ons_id)
            party_name = recomend['Reco']
            party = PARTIES[party_name]
            if party is not None:
                suggestion = OtherSiteSuggestion(
                    who_suggests='Best for Britain',
                    party=party,
                    url='https://getvoting.org/')
                yield constituency, suggestion

def _tacticalvote_uk():
    with open('data/tacticalvote/recommendations.json') as f:
        data = json.load(f)
        for recomend in data:
            if recomend['VoteFor'] != 'TBC':
                suggestion = OtherSiteSuggestion(
                    who_suggests='tacticalvote.co.uk',
                    party=get_party(recomend['VoteFor']),
                    url='https://tacticalvote.co.uk/#{}'.format(recomend['Constituency'].replace(' ', '')))
                yield get_constitiuency(recomend['id']), suggestion

def _tactical_dot_vote():
    PARTY_RECOMEND = {
	    '<span class="no-recommendation recommendation-sm">No recommendation</span>': None,
        '<span class="not-sure recommendation-sm">Not sure</span>': None,

        '<span class="labour recommendation-sm">Labour</span>': LAB,
        '<span class="scottish-national-party recommendation-sm">Scottish National Party</span>': SNP,
        '<span class="liberal-democrat recommendation-sm">Liberal Democrat</span>': LD,
        '<span class="alliance recommendation-sm">Alliance</span>': ALLIANCE,
        '<span class="sinn-fein recommendation-sm">Sinn Fein</span>': SF,
        '<span class="social-democratic-and-labour-party recommendation-sm">Social Democratic and Labour Party</span>': SDLP,
        '<span class="plaid-cymru recommendation-sm">Plaid Cymru</span>': PLAID,
        '<span class="national-health-action-party recommendation-sm">National Health Action Party</span>': NHAP,
        '<span class="green recommendation-sm">Green</span>': GREEN,
        '<span class="independent recommendation-sm">Independent</span>': INDEPENDENT,
    }
    with open('data/tactical_dot_vote/all.html') as f:
        [table] = re.compile(r'<table class="table">(.*)</table>').findall(f.read())
        tr_list = [
            tr
            for tr in re.compile(r'<tr>(.*?)</tr>').findall(table)
            if '<th>' not in tr]
        assert len(tr_list) == 650
        for row in tr_list:
            url, name, recommendation = re.compile(r'<td><a href="([^"]+)">([^<>]+)</a></td><td>.*?</td><td>(.*?)</td>').search(row).groups()
            party = PARTY_RECOMEND[recommendation]
            if party is not None:
                suggestion = OtherSiteSuggestion(
                    who_suggests='tactical.vote',
                    party=party,
                    url='https://tactical.vote/{}'.format(url))
                yield get_constitiuency_from_name(name), suggestion

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
    # This is actually ordered, because a python dict is secretly an OrderedDict
    out = defaultdict(list)

    # trusted, hand-picked
    for constituency, suggest in _tacticalvote_uk():
        out[constituency].append(suggest)
    for constituency, suggest in _early_pv():
        out[constituency].append(suggest)

    # heavy GE2017 bias (LAB):
    for constituency, suggest in _tactical_dot_vote():
        out[constituency].append(suggest)

    # heavy EP2019 bias (LD):
    for constituency, suggest in _getvoting():
        out[constituency].append(suggest)

    # smaller sites:
    for constituency, suggest in _essex_against_tories():
        out[constituency].append(suggest)

    return dict(out)
