import json
from pathlib import Path
import nltk
import numpy as np

def real_name(name, list_names=[]):
    names = list_names
    lastnames = [[x for x in name.split(' ') if len(x) > 1][-1] for name in names]
    firstnames = [[x for x in name.split(' ') if len(x) > 1][0] for name in names]

    comparison_name, comparison_lastname, comparison_firstname = [], [], []
    for i in range(len(names)):
        comparison_name += [nltk.edit_distance(names[i], name)]
        comparison_lastname += [nltk.edit_distance(lastnames[i], name)]
        comparison_firstname += [nltk.edit_distance(firstnames[i], name)]

    comparison_list = comparison_name + comparison_lastname + comparison_firstname

    return names[np.argmin(comparison_list) % len(names)]