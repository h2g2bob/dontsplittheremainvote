import json
from jinja2 import Environment, FileSystemLoader
from typing import Dict
from typing import List
from .dataset import Dataset
from .load_dataset import datasets_by_constituency
from .load_dataset import get_all_datasets
from .constituency import all_constituencies
from .constituency_page import ConstituencyPage
from .generate_postcode_sqlite import make_sqlite

JINJA_ENV = Environment(loader=FileSystemLoader('templates/'))

BASE_URL = 'https://dontsplittheremainvote.com'
STATIC = "/static"
IMAGE_LOGO_600_314 = BASE_URL + STATIC + '/banner/banner_600_314.png'
IMAGE_LOGO_735_238 = BASE_URL + STATIC + '/banner/banner_735_285.png'

def generate_all_constituencies():
    make_sqlite()

    constituency_pages = datasets_by_constituency()
    for constituency_page in constituency_pages:
        nearby_constituencies = _nearby_constituencies(constituency_pages, constituency_page.constituency)
        generate_constituency(constituency_page, nearby_constituencies)
    generate_index(constituency_pages)
    generate_json(constituency_pages)

    datasets = get_all_datasets()
    generate_datasets(datasets)

def _sanity(constituency_page):
    parties = tuple(set(oth.party for oth in constituency_page.other_site_suggestions))
    if len(parties) > 1:
        print("Our external sources contracict! {}".format(constituency_page.constituency.slug))
    if len(parties) > 0:
        their_advice = {p.short for p in parties}
        our_advice = constituency_page.advice.template
        if our_advice in ('alliance-mixed.html', 'leave.html', 'remain.html', 'contradict.html', 'special-ignore-polling.html', 'special-contradict-polling.html'):
            pass # no advice
        elif our_advice.split('-')[-1].replace('.html', '') in their_advice:
            pass # same advice
        else:
            print("{} {} != {}".format(constituency_page.constituency.slug, constituency_page.advice.template, their_advice))

def _nearby_constituencies(constituency_pages, constituency):
    rcc = region_county_constituency(constituency_pages)
    same_county = rcc[constituency.region][constituency.county]
    return [cpg.constituency for cpg in same_county if cpg.constituency.slug != constituency.slug]

def generate_constituency(constituency_page, nearby_constituencies):
    _sanity(constituency_page)
    url_path = '/constituency/{}.html'.format(constituency_page.constituency.slug)
    html = JINJA_ENV.get_template(constituency_page.advice.template).render(
        static=STATIC,
        this_url=BASE_URL + url_path,
        image_735_385=IMAGE_LOGO_735_238,
        constituency=constituency_page.constituency,
        datasets=constituency_page.datasets,
        outcomes=constituency_page.outcomes,
        advice=constituency_page.advice,
        other_sites=constituency_page.other_site_suggestions,
        nearby_constituency=nearby_constituencies,
        known_ppc=constituency_page.known_ppc,
        **constituency_page.advice.advice_kwargs)
    with open('generated' + url_path, 'w') as f:
        f.write(html)

def region_county_constituency(constituency_pages: List[ConstituencyPage]) -> Dict[str, Dict[str, List[ConstituencyPage]]]:
    by_region_and_county = {}
    for cp in constituency_pages:
        by_region_and_county \
            .setdefault(cp.constituency.region, {}) \
            .setdefault(cp.constituency.county, []) \
            .append(cp)
    return by_region_and_county

def generate_index(constituency_pages):
    for output_path, template_path in [
        ('constituency/index.html', 'constituency_index.html'),
        ('index.html', 'main_index.html'),
        ('contact.html', 'contact.html'),
    ]:
        html = JINJA_ENV.get_template(template_path).render(
            static=STATIC,
            this_url=BASE_URL + '/',
            image_735_385=IMAGE_LOGO_735_238,
            constituency_pages=region_county_constituency(constituency_pages))
        with open('generated/' + output_path, 'w') as f:
            f.write(html)

def generate_datasets(datasets: List[Dataset]):
    html = JINJA_ENV.get_template('datasets.html').render(
        static=STATIC,
        this_url=BASE_URL + '/datasets.html',
        image_735_385=IMAGE_LOGO_735_238,
        datasets=datasets)
    with open('generated/datasets.html', 'w') as f:
        f.write(html)

def generate_json(constituency_pages: List[ConstituencyPage]):
    constituencies_data = {
        cpage.constituency.slug: cpage.as_json()
        for cpage in constituency_pages
    }
    data = {
        '_info':
            'This is a representation of the internal state of DontSplit.'
            + ' It is useful if you want to track changes between revisions'
            + ' but I don\'t guarantee backwards compatibiltiy or a stable API!',
        'constituencies': constituencies_data}
    with open('generated/data.json', 'w') as f:
        f.write(json.dumps(data, indent=2, sort_keys=True))
