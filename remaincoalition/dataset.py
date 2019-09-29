from . import data_ge2017
from . import data_ge2017 as data_ge2015
from .constituency import all_constituencies

def get_all_datasets():
    datasets = {
        "ge2015": data_ge2015.get_data(),
        "ge2017": data_ge2017.get_data()}
    return datasets

def datasets_by_constituency():
    datasets = get_all_datasets()
    return {
        constituency: {
            dataset_name: results_by_constituency[constituency]
            for dataset_name, results_by_constituency in datasets.items()}
        for constituency in all_constituencies()}

if __name__ == '__main__':
    from .constituency import get_constitiuency
    print(repr(datasets_by_constituency()[get_constitiuency('E14001062')]))
