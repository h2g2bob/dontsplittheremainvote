from . import data_ge2015
from . import data_ge2017
from . import data_ge2019
from . import data_eu2019
from . import data_adj_avg
from . import data_adj_con
from . import data_adj_lab
from . import data_adj_ld
from . import data_adj_bx
from . import data_adj_ni
from .constituency import all_constituencies
from .constituency import Constituency
from .constituency_page import ConstituencyPage
from .dataset import Dataset
from .other_sites import get_other_site_suggestions
from .pacts import Pact
from .pacts import get_pacts
from .ppc import candidate_data
from .result import Result
from typing import List

def get_all_datasets():
    datasets = [
        data_ge2017.DATA_2017,
        data_ge2015.DATA_2015,
        data_eu2019.DATA_2019,

        data_adj_avg.DATA_2017,
        data_adj_avg.DATA_2015,
        data_adj_avg.DATA_2019,

        data_adj_ld.DATA_2017,
        data_adj_lab.DATA_2017,
        data_adj_con.DATA_2017,
        data_adj_bx.DATA_2017,

        data_adj_ni.DATA_2017,

        data_adj_ld.DATA_2019,
        data_adj_lab.DATA_2019,
    ]
    return datasets

def datasets_by_constituency() -> List[ConstituencyPage]:
    all_datasets = get_all_datasets()
    known_ppc = candidate_data()
    other_sites = get_other_site_suggestions()
    pacts = get_pacts()
    constituency_pages = []
    for constituency in all_constituencies():
        constituency_datasets = {
            dataset: dataset.results_by_constituency[constituency].collect_others(0.02)
            for dataset in all_datasets
            if constituency in dataset.results_by_constituency}
        result_datasets = {
            data_ge2019.DATA_2019: data_ge2019.DATA_2019.results_by_constituency[constituency]
        }
        constituency_pages.append(ConstituencyPage(
            constituency=constituency,
            datasets=constituency_datasets,
            result_datasets=result_datasets,
            other_site_suggestions=other_sites.get(constituency, []),
            known_ppc=known_ppc[constituency],
            pacts=pacts[constituency]))
    return constituency_pages
