import json
import re
from collections import defaultdict
from typing import NamedTuple
from typing import List
from typing import Dict
from .constituency import Constituency
from .constituency import all_constituencies
from .constituency import get_constitiuency
from .constituency import get_constitiuency_from_name
from .constituency import get_constitiuency_from_slug
from .party import Party
from .party import get_party
from .party import ALLIANCE
from .party import CLAIREWRIGHT
from .party import CHANGEUK
from .party import DAVIDGAUKE
from .party import DOMINICGRIEVE
from .party import GAVINSHUKER
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
from .party import SPEAKER
from .party import UUP

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


class Aggregation(NamedTuple):
    """The advice box at the top of the page"""
    template: str
    party: Party = None
    provisional: bool = True

    def as_json(self):
        return {
            'template': self.template,
            'party': self.party.short if self.party is not None else None,
        }


def dontsplit_suggestion(party: Party, constituency: Constituency) -> OtherSiteSuggestion:
    return OtherSiteSuggestion(
            who_suggests='Don\'t Split the Remain Vote',
            party=party,
            url='https://dontsplittheremainvote.com/constituency/{}.html#Analysis'.format(constituency.slug))

def _getvoting():
    PARTIES = {
        'Anna Soubry': CHANGEUK,
        'Antoinette Sandbach': LD, # former conservative, now LD
        'Claire Wright': CLAIREWRIGHT,
        'David Gauke': DAVIDGAUKE, # former conservative - maybe not standing again?
        'Dominic Grieve': DOMINICGRIEVE, # former conservative (pact with LD)
        'Gavin Shuker': GAVINSHUKER, # former labour
        'Green': GREEN,
        'Lab': LAB,
        'Lib Dem': LD,
        'LibLab': None, # "Either LD or LAB"
        'Lindsey Hoyle': None, # Speaker, so "no recommendation"
        'none': None,
        'Philip Hammond': INDEPENDENT, # former conservative, but he decided to stand down
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
            if recomend['VoteFor'] not in ['TBC', 'Any']:
                suggestion = OtherSiteSuggestion(
                    who_suggests='tacticalvote.co.uk',
                    party=get_party(recomend['VoteFor']),
                    url='https://tacticalvote.co.uk/#{}'.format(recomend['Constituency'].replace(' ', '')))
                yield get_constitiuency(recomend['id']), suggestion

def _tactical_dot_vote():
    PARTY_RECOMEND = {
        '<span class="no-recommendation recommendation-sm">No recommendation</span>': None,
        '<span class="no-recommendation recommendation-sm">None</span>': None,
        '<span class="not-sure recommendation-sm">Not sure</span>': None,
        '<span class="labour recommendation-sm">Labour</span>': LAB,
        '<span class="scottish-national-party recommendation-sm">Scottish National Party</span>': SNP,
        '<span class="scottish-national-party recommendation-sm">SNP</span>': SNP,
        '<span class="liberal-democrat recommendation-sm">Liberal Democrat</span>': LD,
        '<span class="liberal-democrat recommendation-sm">Lib Dem</span>': LD,
        '<span class="alliance recommendation-sm">Alliance</span>': ALLIANCE,
        '<span class="sinn-fein recommendation-sm">Sinn Fein</span>': SF,
        '<span class="social-democratic-and-labour-party recommendation-sm">Social Democratic and Labour Party</span>': SDLP,
        '<span class="social-democratic-and-labour-party recommendation-sm">SDLP</span>': SDLP,
        '<span class="plaid-cymru recommendation-sm">Plaid Cymru</span>': PLAID,
        '<span class="plaid-cymru recommendation-sm">Plaid</span>': PLAID,
        '<span class="national-health-action-party recommendation-sm">National Health Action Party</span>': NHAP,
        '<span class="green recommendation-sm">Green</span>': GREEN,
        '<span class="independent recommendation-sm">Independent</span>': INDEPENDENT,
    }
    with open('data/tactical_dot_vote/all.html') as f:
        [table] = re.compile(r'<table class="table mt-3" id="list">(.*)</table>', re.DOTALL).findall(f.read())
        tr_list = [
            tr
            for tr in re.compile(r'<tr>(.*?)</tr>').findall(table)
            if '<th>' not in tr]
        assert len(tr_list) == 650
        for row in tr_list:
            url, name, recommendation = re.compile(r'<td><a href="([^"]+)">([^<>]+)</a></td><td>.*?</td><td>(.*?)</td>').search(row).groups()
            party = PARTY_RECOMEND[recommendation]

            if party is not None:
                constituency = get_constitiuency_from_name(name)

                if constituency.slug == 'east-devon' and party == INDEPENDENT:
                    party = CLAIREWRIGHT

                suggestion = OtherSiteSuggestion(
                    who_suggests='tactical.vote',
                    party=party,
                    url='https://tactical.vote/{}'.format(url))
                yield constituency, suggestion


_REMAINUTD = {
    'Vote Labour': LAB,
    'Vote SNP': SNP,
    'Vote Sinn Fein': SF,
    'Vote Lib Dem': LD,
    'Vote Plaid Cymru': PLAID,
    'Vote Alliance': ALLIANCE,
    'Vote Claire Wright (Ind)': CLAIREWRIGHT,

    'For the best chance of reducing the Conservative majority, vote Labour': LAB,
    'For the best chance of reducing the Conservative majority, vote Lib Dem': LD,
    'For the best chance of reducing the DUP majority, vote Sinn Fein': SF,
    'For the best chance of reducing the DUP majority, vote Alliance': ALLIANCE,

    'Voter choice - Lib Dem or Lab ': None,
    'seat hard to predict due to prominent Independent candidate': None,
    'Conservative-Independent seat': None, # no explanation - eg: east devon
}
def _remainunited():
    for constituency in all_constituencies():
        with open('data/remainunited/response/{}.html'.format(constituency.slug)) as f:
            page = f.read()

            if 'Postcode could not be matched' in page:
                print('Postcode not mached {}'.format(constituency.slug))
                continue
            if 'Seat ID could not be matched to Tactical Data' in page:
                print('Error from remainunited {}'.format(constituency.slug))
                continue

            try:
                [answer1, answer2] = re.compile(r'<p class="question">Recommendation</p>\s*<p class="answer">(.*?)</p>').findall(page)
            except ValueError:
                raise ValueError('Bad file {}'.format(constituency.slug))

            if answer1 != answer2:
                raise Exception((constituency, answer1, answer2))
            if answer1 == 'No recommendation':
                continue

            party = _REMAINUTD[answer1]
            if party is None:
                continue

            postcode = re.compile(r'<p class="question">Your Postcode</p>\s*<p class="answer">([^<>]+)</p>').findall(page)[0]
            suggest = OtherSiteSuggestion(
                who_suggests='Remain United',
                party=party,
                url='https://www.remainunited.org/#postcode=' + postcode)
            yield constituency, suggest


_PEOPLES_VOTE = {
    'Alliance': ALLIANCE,
    'Aled ap Dafydd': PLAID,
    'Anna Soubry': CHANGEUK,
    'Claire Wright': CLAIREWRIGHT,
    'Dominic Grieve': DOMINICGRIEVE,
    'Green Party': GREEN,
    'Labour': LAB,
    'Liberal Democrats': LD,
    'Martin Goss': LD,
    'Paul Follows': LD,
    'Plaid Cymru': PLAID,
    'Sinn Féin': SF,
    'Social Democratic and Labour Party': SDLP,
    'Speaker': SPEAKER,
    'Ulster Unionist Party': UUP,
    'Vix Lowthion': GREEN,
}
def _peoples_vote():
    for constituency in all_constituencies():
        with open('data/peoples_vote/response/{}.html'.format(constituency.slug)) as f:
            page = f.read()

            if '<h3>Coming soon</h3>' in page:
                continue
            if 'we haven’t made a recommendation in your constituency yet' in page:
                continue
            if 'Please check you\'ve entered your postcode correctly' in page:
                print('Bad postcode for PV {}'.format(constituency.slug))
                continue

            try:
                [url] = re.compile(r'<meta property="og:url" content="(/[^"]+)" />').search(page).groups()
                [vote_for_person, vote_for_party] = re.compile(r'<div class="reason">\s*<strong>VOTE for</strong> (.*)\s+\((.*)\)\s*</div>').search(page).groups()

                if vote_for_person == '' and vote_for_party == 'Independent': # belfast-west
                    continue

                if vote_for_party == 'Independent':
                    party = _PEOPLES_VOTE[vote_for_person]
                else:
                    party = _PEOPLES_VOTE[vote_for_party]

            except Exception:
                print(constituency.slug)
                raise

            suggest = OtherSiteSuggestion(
                who_suggests='People\'s Vote',
                party=party,
                url='https://tactical-vote.uk' + url)
            yield constituency, suggest


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


def _jonworth():
    results = [
        # (i) Unusual Seats
        ('ashfield', LAB),
        ('finchley-and-golders-green', LD),
        ('leicester-east', LAB),

        # (ii) Seats with prominent independents and/or incumbents running
        ('beaconsfield', DOMINICGRIEVE),
        ('east-devon', CLAIREWRIGHT),
        ('eddisbury', LD),
        ('south-west-hertfordshire', DAVIDGAUKE),

        # (iii) Three way marginals with Conservative incumbents, Labour 2nd in 2017
        ('altrincham-and-sale-west', LD),
        ('chelsea-and-fulham', LD),
        ('cities-of-london-and-westminster', LD),
        ('esher-and-walton', LD),
        ('henley', LD),
        ('hitchin-and-harpenden', LD),
        ('newton-abbot', LD),
        ('north-east-somerset', LD),
        ('south-east-cambridgeshire', LD),
        ('south-east-cornwall', LD),
        ('southport', LD),
        ('st-austell-and-newquay', LD),
        ('woking', LD),

        ('wimbledon', LD),
        ('wantage', LD),

        # ('ashfield', LAB) again
        ('elmet-and-rothwell', LAB),
        ('macclesfield', LAB),

        ('rushcliffe', LAB),

        # (iv) Other three way marginals
        ('bury-st-edmunds', LAB),
    ]
    for slug, party in results:
        if party is not None:
            yield [
                get_constitiuency_from_slug(slug),
                OtherSiteSuggestion(
                    who_suggests='Jon Worth',
                    party=party,
                    url='https://jonworth.eu/2019-uk-general-election-tactical-voting-guide/')]


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

    # 
    for constituency, suggest in _remainunited():
        out[constituency].append(suggest)

    # 
    for constituency, suggest in _peoples_vote():
        out[constituency].append(suggest)

    # smaller sites:
    for constituency, suggest in _jonworth():
        out[constituency].append(suggest)
    for constituency, suggest in _essex_against_tories():
        out[constituency].append(suggest)

    return dict(out)
