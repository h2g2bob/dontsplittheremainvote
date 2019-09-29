from jinja2 import Environment, FileSystemLoader
from .dataset import datasets_by_constituency
from .constituency import all_constituencies

JINJA_ENV = Environment(loader=FileSystemLoader('templates/'))

def generate_all_constituencies():
    for constituency, datasets in datasets_by_constituency().items():
        generate_constituency(constituency, datasets)

def generate_constituency(constituency, datasets):
    html = JINJA_ENV.get_template('constituency.html').render(
        constituency=constituency,
        datasets=datasets)
    with open('generated/{}.html'.format(constituency.slug), 'w') as f:
        f.write(html)
