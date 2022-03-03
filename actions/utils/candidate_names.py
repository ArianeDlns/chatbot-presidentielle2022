import json
from pathlib import Path
import nltk
import numpy as np

candidates_data = json.loads(Path("/app/actions/data/data_candidates/candidates.json").read_text())
candidates_name = [candidate['name']
                   for candidate in candidates_data['candidates']]

def real_name(name, list_names=[]):
    if len(list_names)>0:
        names = list_names
    else:
        names = candidates_name

    comparaison_name = []
    for real_name in names:
        comparaison_name += [nltk.edit_distance(real_name, name)]
    print(np.min(comparaison_name))
    idx = np.argmin(comparaison_name)

    return names[idx]