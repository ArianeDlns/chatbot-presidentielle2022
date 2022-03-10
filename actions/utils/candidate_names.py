import json
from pathlib import Path
import nltk
import numpy as np

candidates_data = json.loads(Path("actions/data/data_candidates/candidates.json").read_text())
candidates_name = [candidate['name']
                   for candidate in candidates_data['candidates']]

def real_name(name, list_names=[]):
    if len(list_names)>0:
        names = list_names
    else:
        names = candidates_name
    lastnames = [[x for x in name.split(' ') if len(x) > 1][-1] for name in names]
    firstnames = [[x for x in name.split(' ') if len(x) > 1][0] for name in names]

    comparison_name, comparison_lastname, comparison_firstname = [], [], []
    for i in range(len(names)):
        comparison_name += [nltk.edit_distance(names[i], name)]
        comparison_lastname += [nltk.edit_distance(lastnames[i], name)]
        comparison_firstname += [nltk.edit_distance(firstnames[i], name)]

    comparison_list = comparison_name + comparison_lastname + comparison_firstname

    return names[np.argmin(comparison_list) % len(names)]