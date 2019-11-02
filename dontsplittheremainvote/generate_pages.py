import csv
import json
from jinja2 import Environment, FileSystemLoader
from typing import Dict
from typing import List
from typing import Tuple
from .dataset import Dataset
from .load_dataset import datasets_by_constituency
from .load_dataset import get_all_datasets
from .constituency import all_constituencies
from .constituency import Constituency
from .constituency_page import ConstituencyPage
from .generate_postcode_sqlite import make_sqlite
from .party import Party

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
    generate_other_sites_csv(constituency_pages)

    datasets = get_all_datasets()
    generate_datasets(datasets)

def _nearby_constituencies(constituency_pages, constituency):
    rcc = region_county_constituency(constituency_pages)
    same_county = rcc[constituency.region][constituency.county]
    return [cpg.constituency for cpg in same_county if cpg.constituency.slug != constituency.slug]

def generate_constituency(constituency_page, nearby_constituencies):
    url_path = '/constituency/{}.html'.format(constituency_page.constituency.slug)

    html = JINJA_ENV.get_template('constituency.html').render(
        static=STATIC,
        this_url=BASE_URL + url_path,
        image_735_385=IMAGE_LOGO_735_238,
        constituency=constituency_page.constituency,
        datasets_election=constituency_page.datasets_election,
        datasets_polling=constituency_page.datasets_polling,
        outcomes=constituency_page.outcomes,
        other_sites=constituency_page.other_site_suggestions,
        nearby_constituency=nearby_constituencies,
        known_ppc=constituency_page.known_ppc,
        analysis=constituency_page.analysis,
        aggregation=constituency_page.aggregation)
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

def _generate_other_sites_data(constituency_pages: List[ConstituencyPage]) -> Tuple[Tuple[str], Dict[Constituency, Dict[str, Party]]]:
    """
    suggestions_by_constituency = {
        Constituency: { site_name : Party },
    }
    """
    suggestions_by_constituency = {}
    all_site_names = set()
    for cpage in constituency_pages:
        suggestions_here = {
            sug.who_suggests: sug.party
            for sug in cpage.other_site_suggestions}

        we_recommend_party = cpage.analysis.we_recommend_party
        if we_recommend_party is not None:
            suggestions_here['DontSplit main'] = we_recommend_party

        suggestions_by_constituency[cpage.constituency] = suggestions_here
        all_site_names |= suggestions_here.keys()
    return tuple(sorted(all_site_names)), suggestions_by_constituency

def generate_other_sites_csv(constituency_pages: List[ConstituencyPage]):
    all_site_names, all_suggestions = _generate_other_sites_data(constituency_pages)
    with open('generated/other_sites.csv', 'w') as f:
        writer = csv.writer(f)

        headers = ['constituency', 'ons_id']
        for site_name in all_site_names:
            headers.append(site_name)
            headers.append(site_name + " alignment")
        writer.writerow(headers)

        for constituency, con_sugg in all_suggestions.items():
            data = [constituency.slug, constituency.ons_id]
            for site_name in all_site_names:
                try:
                    party = con_sugg[site_name]
                    alignment = sum(
                        +1 if site_sugg == party else -1
                        for site_sugg in con_sugg.values())
                    alignment -= 1  # you match your own recommendation!
                except KeyError:
                    party = None
                    alignment = None
                data.append(party.short if party is not None else None)
                data.append(alignment)
            writer.writerow(data)
