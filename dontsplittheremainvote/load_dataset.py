from . import data_ge2015
from . import data_ge2015_adjust_avg
from . import data_ge2017
from . import data_ge2017_adjust_avg
from . import data_adj_con
from . import data_adj_lab
from . import data_adj_ld
from . import data_adj_bx
from .constituency import all_constituencies
from .constituency import Constituency
from .dataset import Dataset
from .result import Result
from typing import Dict

def get_all_datasets():
    datasets = {
        data_ge2017.DESCRIPTION: data_ge2017.get_data(),
        data_ge2015.DESCRIPTION: data_ge2015.get_data(),
        data_ge2017_adjust_avg.DESCRIPTION: data_ge2017_adjust_avg.get_data(),
        data_ge2015_adjust_avg.DESCRIPTION: data_ge2015_adjust_avg.get_data(),
        data_adj_con.DESCRIPTION_2017: data_adj_con.get_data_2017(),
        data_adj_lab.DESCRIPTION_2017: data_adj_lab.get_data_2017(),
        data_adj_ld.DESCRIPTION_2017: data_adj_ld.get_data_2017(),
        data_adj_bx.DESCRIPTION_2017: data_adj_bx.get_data_2017(),
    }
    return datasets

def datasets_by_constituency() -> Dict[Constituency, Dict[Dataset, Result]]:
    datasets = get_all_datasets()
    return {
        constituency: {
            dataset_name: results_by_constituency[constituency]
            for dataset_name, results_by_constituency in datasets.items()}
        for constituency in all_constituencies()}
