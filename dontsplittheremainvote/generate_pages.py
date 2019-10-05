from jinja2 import Environment, FileSystemLoader
from .load_dataset import datasets_by_constituency
from .constituency import all_constituencies

JINJA_ENV = Environment(loader=FileSystemLoader('templates/'))

def generate_all_constituencies():
    for constituency_page in datasets_by_constituency():
        generate_constituency(constituency_page)

def generate_constituency(constituency_page):
    html = JINJA_ENV.get_template('constituency.html').render(
        constituency=constituency_page.constituency,
        datasets=constituency_page.datasets,
        outcomes=constituency_page.outcomes(),
        advice=constituency_page.advice())
    with open('generated/constituency/{}.html'.format(constituency_page.constituency.slug), 'w') as f:
        f.write(html)
