from jinja2 import Environment, FileSystemLoader
from typing import List
from .dataset import Dataset
from .load_dataset import datasets_by_constituency
from .load_dataset import get_all_datasets
from .constituency import all_constituencies
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
        generate_constituency(constituency_page)
    generate_index(constituency_pages)

    datasets = get_all_datasets()
    generate_datasets(datasets)

def _sanity(constituency_page):
    parties = tuple(set(oth.party for oth in constituency_page.other_site_suggestions))
    if len(parties) > 1:
        raise ValueError("Our external sources contracict! {}".format(constituency_page.constituency.slug))
    if len(parties) == 1:
        their_advice = parties[0].short
        our_advice = constituency_page.advice.template
        if our_advice in ('alliance-mixed.html', 'leave.html', 'remain.html'):
            pass # no advice
        elif our_advice.split('-')[-1].replace('.html', '') == their_advice:
            pass # same advice
        else:
            raise ValueError("{} {} != {}".format(constituency_page.constituency.slug, constituency_page.advice.template, their_advice))

def generate_constituency(constituency_page):
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
        **constituency_page.advice.advice_kwargs)
    with open('generated' + url_path, 'w') as f:
        f.write(html)

def generate_index(constituency_pages):
    html = JINJA_ENV.get_template('constituency_index.html').render(
        static=STATIC,
        this_url=BASE_URL + '/',
        image_735_385=IMAGE_LOGO_735_238,
        constituency_pages=constituency_pages)
    with open('generated/index.html', 'w') as f:
        f.write(html)
    with open('generated/constituency/index.html', 'w') as f:
        f.write(html)

def generate_datasets(datasets: List[Dataset]):
    html = JINJA_ENV.get_template('datasets.html').render(
        static=STATIC,
        this_url=BASE_URL + '/datasets.html',
        image_735_385=IMAGE_LOGO_735_238,
        datasets=datasets)
    with open('generated/datasets.html', 'w') as f:
        f.write(html)
