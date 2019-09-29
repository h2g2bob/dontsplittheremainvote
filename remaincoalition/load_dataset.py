from . import data_ge2015
from . import data_ge2017
from .constituency import all_constituencies
from .constituency import Constituency
from .dataset import Dataset
from .result import Result
from typing import Dict

def get_all_datasets():
    datasets = {
        data_ge2017.DESCRIPTION: data_ge2017.get_data(),
        data_ge2015.DESCRIPTION: data_ge2015.get_data(),
    }
    return datasets

def datasets_by_constituency() -> Dict[Constituency, Dict[Dataset, Result]]:
    datasets = get_all_datasets()
    return {
        constituency: {
            dataset_name: results_by_constituency[constituency]
            for dataset_name, results_by_constituency in datasets.items()}
        for constituency in all_constituencies()}
