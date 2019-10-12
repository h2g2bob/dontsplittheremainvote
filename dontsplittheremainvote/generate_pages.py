from jinja2 import Environment, FileSystemLoader
from typing import List
from .dataset import Dataset
from .load_dataset import datasets_by_constituency
from .load_dataset import get_all_datasets
from .constituency import all_constituencies
from .generate_postcode_sqlite import make_sqlite

JINJA_ENV = Environment(loader=FileSystemLoader('templates/'))

def generate_all_constituencies():
    make_sqlite()

    constituency_pages = datasets_by_constituency()
    for constituency_page in constituency_pages:
        generate_constituency(constituency_page)
    generate_index(constituency_pages)

    datasets = get_all_datasets()
    generate_datasets(datasets)

def generate_constituency(constituency_page):
    html = JINJA_ENV.get_template(constituency_page.advice.template).render(
        static="/static",
        constituency=constituency_page.constituency,
        datasets=constituency_page.datasets,
        outcomes=constituency_page.outcomes,
        advice=constituency_page.advice,
        **constituency_page.advice.advice_kwargs)
    with open('generated/constituency/{}.html'.format(constituency_page.constituency.slug), 'w') as f:
        f.write(html)

def generate_index(constituency_pages):
    html = JINJA_ENV.get_template('constituency_index.html').render(
        static="/static",
        constituency_pages=constituency_pages)
    with open('generated/index.html', 'w') as f:
        f.write(html)
    with open('generated/constituency/index.html', 'w') as f:
        f.write(html)

def generate_datasets(datasets: List[Dataset]):
    html = JINJA_ENV.get_template('datasets.html').render(
        static="/static",
        datasets=datasets)
    with open('generated/datasets.html', 'w') as f:
        f.write(html)
