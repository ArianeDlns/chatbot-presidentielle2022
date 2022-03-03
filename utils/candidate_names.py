import json
from pathlib import Path
import nltk
import numpy as np

candidates_data = json.loads(Path("data/data_candidates/candidates.json").read_text())
candidates_name = [candidate['name']
                   for candidate in candidates_data['candidates']]

def real_name(name, list_names=[]):
    if len(list_names)>0:
        names = list_names
    else:
        names = candidates_name
    lastnames = [name.split(' ')[-1] for name in names]


    comparison_name, comparison_lastname = [], []
    for i in range(len(names)):
        comparison_name += [nltk.edit_distance(names[i], name)]
        comparison_lastname += [nltk.edit_distance(lastnames[i], name)]

    min1, min2 = np.min(comparison_name), np.min(comparison_lastname)
    if min1 < min2:
        return names[np.argmin(comparison_name)]
    else:
        return names[np.argmin(comparison_lastname)]
