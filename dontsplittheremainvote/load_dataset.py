from . import data_ge2015
from . import data_ge2017
from . import data_eu2019
from . import data_adj_con
from . import data_adj_lab
from . import data_adj_ld
from . import data_adj_bx
from . import data_adj_avg
from .constituency import all_constituencies
from .constituency import Constituency
from .constituency_page import ConstituencyPage
from .dataset import Dataset
from .result import Result
from typing import List

def get_all_datasets():
    datasets = {
        data_ge2017.DESCRIPTION: data_ge2017.get_data(),
        data_ge2015.DESCRIPTION: data_ge2015.get_data(),
        data_eu2019.DESCRIPTION: data_eu2019.get_data(),

        data_adj_avg.DESCRIPTION_2017: data_adj_avg.get_data_2017(),
        data_adj_avg.DESCRIPTION_2015: data_adj_avg.get_data_2015(),
        data_adj_avg.DESCRIPTION_2019: data_adj_avg.get_data_2019(),

        data_adj_con.DESCRIPTION_2017: data_adj_con.get_data_2017(),
        data_adj_lab.DESCRIPTION_2017: data_adj_lab.get_data_2017(),
        data_adj_ld.DESCRIPTION_2017: data_adj_ld.get_data_2017(),
        data_adj_bx.DESCRIPTION_2017: data_adj_bx.get_data_2017(),
    }
    return datasets

def datasets_by_constituency() -> List[ConstituencyPage]:
    all_datasets = get_all_datasets()
    constituency_pages = []
    for constituency in all_constituencies():
        constituency_datasets = {
            dataset_name: results_by_constituency[constituency].collect_others(0.02)
            for dataset_name, results_by_constituency in all_datasets.items()
            if constituency in results_by_constituency}
        constituency_pages.append(ConstituencyPage(
            constituency=constituency,
            datasets=constituency_datasets))
    return constituency_pages
