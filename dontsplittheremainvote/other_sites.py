import glob
import json
import re
from collections import defaultdict
from typing import NamedTuple
from typing import List
from typing import Dict
from typing import Optional
from .constituency import Constituency
from .constituency import all_constituencies
from .constituency import get_constitiuency
from .constituency import get_constitiuency_from_name
from .constituency import get_constitiuency_from_slug
from .party import Party
from .party import get_party
from .party import ALLIANCE
from .party import ANNASOUBRY
from .party import ANYPARTY
from .party import CLAIREWRIGHT
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
    they_say: Optional[str] = None
    important: bool = False

    def as_json(self):
        return {
            'who_suggests': self.who_suggests,
            'party': self.party.short,
            'url': self.url,
            'they_say': self.they_say,
            'important': self.important,
        }


class Aggregation(NamedTuple):
    """The advice box at the top of the page"""
    template: str
    party: Party = None
    provisional: bool = True
    important: bool = False
    disagreement: bool = False

    def as_json(self):
        return {
            'template': self.template,
            'party': self.party.short if self.party is not None else None,
            'important': self.important,
            'disagreement': self.disagreement,
        }


def dontsplit_suggestion(party: Party, constituency: Constituency) -> OtherSiteSuggestion:
    return OtherSiteSuggestion(
            who_suggests='Don\'t Split the Remain Vote',
            party=party,
            url='https://dontsplittheremainvote.com/2019/constituency/{}.html#Analysis'.format(constituency.slug))


_POSTCODE_EXAMPLES = {}
def example_postcode(constituency: Constituency):
    if not _POSTCODE_EXAMPLES:
        with open('generated/example_postcodes.csv') as f:
            pairs = (line.strip().split(',') for line in f)
            _POSTCODE_EXAMPLES.update({
                slug: postcode
                for slug, postcode in pairs})
    return _POSTCODE_EXAMPLES[constituency.slug]


def _getvoting_pages(page: str) -> Party:
    PARTIES = {
        'The Labour Party': LAB,
        'The Liberal Democrats': LD,
        'Plaid Cymru': PLAID,
        'Dominic Grieve': DOMINICGRIEVE,
        'The Green Party': GREEN,
        'Anna Soubry': ANNASOUBRY,
        'Claire Wright, the independent': CLAIREWRIGHT,
        'Gavin Shuker': GAVINSHUKER,
        'David Gauke': DAVIDGAUKE,
        'SNP': SNP,
        'Scottish Liberal Democrats': LD,
        'Scottish Labour': LAB,
    }

    if '<h2>we are sorry but the page you requested does not exist</h2>' in page:
        raise ValueError("404")

    if '<p class="h4">You can stop Boris Johnson getting a majority if you vote' in page and '<p class="h5">Use your vote for any of:' in page:
        return None

    if '<p class="h4">Many parties and candidates in Northern Ireland are Pro-European but some would not take their seats in the UK Parliament if elected.<br></p>' in page and '<p class="h5">We want to avoid making confusing, inaccurate or counter-productive recommendations.</p>' in page:
        return None

    if '<p class="h4">In your area, both Labour or the Liberal Democrats could win and both have excellent pro-European credentials. We take note of your current MP\'s excellent record on Brexit in Parliament.<br></p>' in page and '<p class="h5">Our data suggests neither the Tories nor the Brexit Party can win here, unlike in other areas, so you can feel safe to vote for whichever pro-EU candidate you prefer.</p>' in page:
        return ANYPARTY

    if '<p class="h4">The main parties generally do not oppose the Speaker, so your current MP is likely to be re-elected<br></p>' in page:
        return None

    if '<p class="h5">We recommend you vote for either the Labour or the Liberal Democrats candidate. Choose either and help a pro-European win.</p>' in page:
        return ANYPARTY

    if '<p class="h5">It\'s difficult to call this one right now. Different seat polls and rounds of MRP show the Liberal Democrats and Labour in different positions. We\'re getting more data and will make a final recommendation before election day.</p>' in page:
        return None

    match = re.compile(r'<p class="h4">Voting for (.*) in your area is the best chance of electing a Pro-EU MP and stopping Brexit.<br></p>').search(page)
    if match is not None:
        [party_name] = match.groups()
        return PARTIES[party_name]

    match = re.compile(r'<p class="h5">We recommend you vote for (.*) candidate</p>').search(page)
    if match is not None:
        [party_name] = match.groups()
        return PARTIES[party_name]

    match = re.compile(r'<p class="h5">This election is about Brexit. Your best chance of stopping a Conservative majority is to vote for the (.*) candidate</p>').search(page)
    if match is not None:
        [party_name] = match.groups()
        return PARTIES[party_name]

    match = re.compile(r'<p class="h5">We recommend you vote for (.*?) candidate\.(?: They are the Unite to Remain Alliance candidate.)?</p>').search(page)
    if match is not None:
        [party_name] = match.groups()
        return PARTIES[party_name]

    raise ValueError(page.split("== SLIDE2")[-1].split("== SLIDE4")[0])

def _getvoting():
    with open('data/getvoting/constituency-names.csv') as f:
        pairs = (line.strip().split(',') for line in f)
        their_slugs = {
            our_slug: their_slug
            for our_slug, their_slug in pairs}

    for constituency in all_constituencies():
        with open('data/getvoting/response/{}.html'.format(constituency.slug)) as f:
            try:
                party = _getvoting_pages(f.read())
            except Exception:
                print(constituency)
                raise
            their_slug = their_slugs[constituency.slug]
            if party is not None:
                suggestion = OtherSiteSuggestion(
                    who_suggests='Best for Britain',
                    party=party,
                    url='https://tacticalvote.getvoting.org/{}/'.format(their_slug))
                yield constituency, suggestion

_TACVOTE_CO_UK = {
    'Alliance': ALLIANCE,
    'Any': ANYPARTY,
    'Claire Wright': CLAIREWRIGHT,
    'Green': GREEN,
    'Labour': LAB,
    'Lib Dem': LD,
    'Plaid Cymru': PLAID,
    'SDLP': SDLP,
    'SNP': SNP,
    'Sinn Féin': SF,
    'TBC': None,
    'No recommendation': None,
    'SNP or Lib Dems': ANYPARTY,
    'Lib Dem or Plaid Cymru': ANYPARTY,
    'SNP or Labour': ANYPARTY,
    'Lib Dem or SNP': ANYPARTY,
    'Labour or SNP': ANYPARTY,
    'Labour or SNP': ANYPARTY,
    'Labour or Lib Dem': ANYPARTY,
}
def _tacticalvote_co_uk():
    with open('data/tacticalvote/recommendations.json') as f:
        data = json.load(f)
        for recomend in data:
            vote_for = recomend['VoteFor']
            if not vote_for:
                continue
            if recomend['VoteFor'] == 'Independent':
                vote_for = recomend['Candidate']
            party = _TACVOTE_CO_UK[vote_for]
            if party is None:
                continue
            suggestion = OtherSiteSuggestion(
                who_suggests='tacticalvote.co.uk',
                party=party,
                url='https://tacticalvote.co.uk/#{}'.format(recomend['Constituency'].replace(' ', '')),
                they_say=recomend['Why'],
                important=(int(recomend['Priority']) == 1))
            yield get_constitiuency(recomend['id']), suggestion

def _tactical_dot_vote():
    PARTY_RECOMEND = {
        '<span class="no-recommendation recommendation-sm">No recommendation</span>': ANYPARTY,
        '<span class="no-recommendation recommendation-sm">None</span>': ANYPARTY,
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
    'Vote Green': GREEN,

    'For the best chance of reducing the Conservative majority, vote Labour': LAB,
    'For the best chance of reducing the Conservative majority, vote Lib Dem': LD,
    'For the best chance of reducing the DUP majority, vote Sinn Fein': SF,
    'For the best chance of reducing the DUP majority, vote Alliance': ALLIANCE,
    'best chance of reducing the Conservative majority, as two parties are tied in second place, wait for 25 Nov update': None,

    'No recommendation': ANYPARTY,
    'Voter choice - Lib Dem or Lab': ANYPARTY,
    'seat hard to predict due to prominent Independent candidate': None,
    'Conservative-Independent seat': None, # no explanation - eg: east devon

    'Momentum with the Independent candidate': INDEPENDENT,
    'Vote Independent': INDEPENDENT,

    'Vote Independent - Dominic Grieve': DOMINICGRIEVE,
    'Vote SF': SF,
    'Vote SDLP': SDLP,
    'For the best chance of reducing the DUP majority, vote SF': SF,
    'Vote Independent - David Gauke': DAVIDGAUKE,
    'For the best chance of reducing or stopping a Tory majority, vote Lib Dem': LD,
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
                [answer1, answer2] = re.compile(r'<p class="question(?: word-wrap)?">Recommendation</p>\s*<p class="answer(?: word-wrap)?">(.*?)</p>').findall(page)
            except ValueError:
                raise ValueError('Bad file {}'.format(constituency.slug))

            if answer1 != answer2:
                raise Exception((constituency, answer1, answer2))

            answer1 = answer1.strip()
            party = _REMAINUTD[answer1]
            if party is None:
                continue

            if party == INDEPENDENT:
                party = {
                    'beaconsfield': DOMINICGRIEVE,
                    'south-west-hertfordshire': DAVIDGAUKE,
                }[constituency.slug]

            postcode = re.compile(r'<p class="question">Your Postcode</p>\s*<p class="answer">([^<>]+)</p>').findall(page)[0]
            [explanation] = re.compile(r'\s+'.join((
                r'<p class="question">Explanation</p>',
                r'<p class="answer">(.*?)</p>'))).search(page).groups()

            explanation = explanation.strip()
            suggest = OtherSiteSuggestion(
                who_suggests='Remain United',
                party=party,
                url='https://www.remainunited.org/#postcode=' + postcode,
                they_say='{} - {}'.format(answer1, explanation))
            yield constituency, suggest


_PEOPLES_VOTE = {
    'Alliance': ALLIANCE,
    'Aled ap Dafydd': PLAID,
    'Anna Soubry': ANNASOUBRY,
    'Claire Wright': CLAIREWRIGHT,
    'David Gauke': DAVIDGAUKE,
    'Dominic Grieve': DOMINICGRIEVE,
    'Green Party': GREEN,
    'Labour': LAB,
    'Liberal Democrats': LD,
    'Martin Goss': LD,
    'Naomi Long': ALLIANCE,
    'Paul Follows': LD,
    'Plaid Cymru': PLAID,
    'Sinn Féin': SF,
    'Social Democratic and Labour Party': SDLP,
    'Sorcha Eastwood': ALLIANCE,
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


def _jonworth():
    pages = {
        'lab-keep': LAB,
        'lab-unseat': LAB,
        'ld-keep': LD,
        'ld-nosplit': LD,
        'ld-unseat': LD,
        'snp-keep': SNP,
        'snp-unseat': SNP,
        'unique': None,
    }

    special_places = {
        'maidenhead': None,
        'ashfield': LAB,
        'north-east-somerset': LD,
        'beaconsfield': DOMINICGRIEVE,
        'south-west-hertfordshire': DAVIDGAUKE,
        'blackley-and-broughton': LAB,
        'southport': None,
        'broxtowe': LAB,
        'watford': None,
        'bury-st-edmunds': LAB,
        'ynys-mon': PLAID,
        'chorley': None,
        'york-outer': None,
        'colchester': None,
        'don-valley': LAB,
        'east-devon': CLAIREWRIGHT,
        'east-lothian': LAB,
        'eddisbury': LD,
        'finchley-and-golders-green': LD,
        'harborough': None,
        'isle-of-wight': GREEN,
        'kensington': LAB,
        'luton-south': LAB,
        'buckingham': LD,
        'ceredigion': ANYPARTY,
        'edinburgh-north-and-leith': SNP,
        'wokingham': LD,
        'arfon': ANYPARTY,
        'sheffield-hallam': ANYPARTY,
        'kirkcaldy-and-cowdenbeath': LAB,
        'midlothian': SNP,
        'cities-of-london-and-westminster': LD,
    }

    # video in wrong section of website *cries*
    wrong_cats = {
        'cheltenham': LD,
    }

    regexp = re.compile(r'<span class="cat-links"><a href="[^"]+" rel="category tag" style="[^"]+">(?P<category>[^<>]+)</a></span>\s+</div>\s+<h3 class="entry-title"><a href="(?P<url>https://tacticalvoting.jonworth.eu/[^"]+/)" rel="bookmark">(?P<constituency>[^<>]+)</a></h3>')

    for page_prefix, page_party in pages.items():
        for page_name in glob.glob('data/jonworth/response/{}.*.html'.format(page_prefix)):
            with open(page_name) as f:
                page = f.read()
                matches = list(regexp.finditer(page))
                if len(matches) == 0:
                    raise ValueError(page_name)
                for match in matches:
                    constituency = get_constitiuency_from_name(match.group('constituency'))
                    if page_party is None:
                        party = special_places[constituency.slug]
                        if party is None:
                            continue
                    else:
                        party = page_party

                    if constituency.slug in wrong_cats:
                        party = wrong_cats[constituency.slug]

                    yield [
                        constituency,
                        OtherSiteSuggestion(
                            who_suggests='Jon Worth (video!)',
                            party=party,
                            url=match.group('url'),
                            they_say=match.group('category'))]


_OBSERVER = {
    'Aberdeen South': SNP,
    'Angus': SNP,
    'Ayr, Carrick and Cumnock': SNP,
    'Banff and Buchan': SNP,
    'Dumfries and Galloway': SNP,
    'East Renfrewshire': SNP,
    'Gordon': SNP,
    'Moray': SNP,
    'Ochil and South Perthshire': SNP,
    'Stirling': SNP,
    'East Lothian': SNP,
    'Kirkcaldy and Cowdenbeath': LAB,
    'Midlothian': SNP,
    'Beaconsfield': DOMINICGRIEVE,
    'Cheadle': LD,
    'Chelsea and Fulham': LD,
    'Cheltenham': LD,
    'Chingford and Woodford Green': LAB,
    'Chipping Barnet': LAB,
    'Cities of London and Westminster': LD,
    'Esher and Walton': LD,
    'Filton and Bradley Stoke': LAB,
    'Finchley and Golders Green': LD,
    'Guildford': LD,
    'Hazel Grove': LD,
    'Hendon': LAB,
    'South West Hertfordshire': DAVIDGAUKE,
    'Lewes': LD,
    'Loughborough': LAB,
    'Putney': LAB,
    'Richmond Park': LD,
    'Rushcliffe': LAB,
    'South Cambridgeshire': LD,
    'Southport': LAB,
    'St Albans': LD,
    'St Ives': LD,
    'Totnes': LD,
    'Truro and Falmouth': LAB,
    'Uxbridge and South Ruislip': LAB,
    'Wantage': LD,
    'Watford': LAB,
    'Wimbledon': LD,
    'Winchester': LD,
    'Wokingham': LD,
    'Wycombe': LAB,
    'York Outer': LAB,
    'Kensington': LD,
    'Portsmouth South': LAB,
    'Sheffield, Hallam': LD,
    'Ynys Môn': LAB,
}
def _observer():
    for slug, party in _OBSERVER.items():
        yield [
            get_constitiuency_from_name(slug),
            OtherSiteSuggestion(
                who_suggests='The Observer',
                party=party,
                url='https://www.theguardian.com/politics/2019/dec/08/tactical-voting-guide-2019-keep-tories-out-remain-voter-general-election')]

def get_other_site_suggestions() -> Dict[Constituency, List[OtherSiteSuggestion]]:
    out = defaultdict(list)

    # trusted, hand-picked, excellent alignment (2 conflicts)
    for constituency, suggest in _tacticalvote_co_uk():
        out[constituency].append(suggest)

    # video! (8 conflicts)
    for constituency, suggest in _jonworth():
        out[constituency].append(suggest)

    # best for britain (EP2019 / LD bias) (14 conflicts)
    for constituency, suggest in _getvoting():
        out[constituency].append(suggest)

    # gina miller (19 conflicts)
    for constituency, suggest in _remainunited():
        out[constituency].append(suggest)

    # 2017 with adjustments (20 conflicts)
    for constituency, suggest in _tactical_dot_vote():
        out[constituency].append(suggest)

    # peoples vote (22 conflicts)
    for constituency, suggest in _peoples_vote():
        out[constituency].append(suggest)

    # guardian (new)
    for constituency, suggest in _observer():
        out[constituency].append(suggest)

    return dict(out)
